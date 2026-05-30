
################################################################################
# NozzleGen — Nozzle Generator Module
# -----------------------------------
# Copyright (C) 2025 Your Name
# Licensed under GPL-3.0-or-later
# See LICENSE file for full terms
#
# Description:
#   This module computes the geometry of a nozzle contour. It generates the
#   x and y coordinates of the nozzle surface based on input parameters:
#   the throat radius, area ratio and number of points (N).
#   This module does NOT perform file I/O or plotting; the driver/CLI handles
#   saving data to .dat files and visualization.
#
# Requirements (before running the code):
#   - Python 3.10 or higher
#   - Pip (to install any missing packages)
#   - Matplotlib (optional, only if visualization is added in the driver)
#
# Notes:
#   - Ensure the LICENSE file is present in the repository root.
#   - This software is distributed WITHOUT ANY WARRANTY; see LICENSE for details.
#
# Author: Andrew Toma
# Date:   2025-10-06
################################################################################

import math
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d



def bellNozzleGenerator(Rt, N, eps, Cr, Lstar, r1, r2, r3, length_percentage, input_thetae):
    # Points list initialization
    xList, yList = [], []

    # Fetching the "thetan" and "thetae" values from the graph
    percentages = np.array([60, 70, 80, 90, 100])

    thetan_values, thetae_values = [], []

    # X-axis interpolation to find the "eps" range
    for p in percentages:
        n_data = pd.read_csv(f"{"Nozzle_Data"}/thetan_{p}.csv") 
        e_data = pd.read_csv(f"{"Nozzle_Data"}/thetae_{p}.csv")

        # Input headers
        n_data.columns = n_data.columns.str.strip().str.replace('\ufeff', '')
        e_data.columns = e_data.columns.str.strip().str.replace('\ufeff', '')
        
        # Create interpolators along epsilon (X) axis
        interp_n = interp1d(n_data["X"], n_data["Y"], kind="linear", fill_value="extrapolate")
        interp_e = interp1d(e_data["X"], e_data["Y"], kind="linear", fill_value="extrapolate")

        # Interpolated theta values at given epsilon
        thetan_values.append(interp_n(eps))
        thetae_values.append(interp_e(eps))


    # Convert lists to arrays for interpolation with scipy
    thetan_values = np.array(thetan_values)
    thetae_values = np.array(thetae_values)


    # Y-axis interpolation to find the "length_percentage" range
    interp_n_vertical = interp1d(percentages, thetan_values, kind="linear", fill_value="extrapolate")
    interp_e_vertical = interp1d(percentages, thetae_values, kind="linear", fill_value="extrapolate")

    # Fetch the values
    thetan = float(interp_n_vertical(length_percentage))
    thetae = float(interp_e_vertical(length_percentage))

    if (input_thetae >= 0):
        thetae = input_thetae

    # Nozzle length "Ln"                                                                                # % of length of conical nozzle, typically 80%
    Ln = (length_percentage / 100) * (math.sqrt(eps) - 1) * Rt / math.tan(math.radians(15))             # Nozzle length (cm)

    # Convergent section angle (degrees)
    theta_conv = 45

    # Nozzle breakdown : N1 = Number of points in the transition from convergent to chamber (r1)
    #                    N2 = Number of points in the transition from throat to convergent (r2)
    #                    N3 = Number of points in the transition from expansion to throat (r3)
    #                    N4 = Number of points in the expansion section (parabola)

    N1 = int (0.1 * N)
    N2 = int (0.15 * N)
    N3 = int (0.2 * N)
    N4 = N - N1 - N2 - N3

    # Add the injector plate (xc) point, if the user provides the characteristic length, r1 and r2
    if (Lstar != 0 and r1 != 0 and r2 != 0):
        # "x1" (the last chamber point) + the chamber length (Lstar / Cr)
        #
        xc = -r2 * Rt * math.sin(math.radians(theta_conv)) - r1 * Rt * math.sin(math.radians(theta_conv)) - (
            (1 / math.tan(math.radians(theta_conv))) * Rt * (math.sqrt(Cr) - 1) - r2 * Rt * (1 - math.cos(math.radians(theta_conv))) - r1 * Rt * (1 - math.cos(math.radians(theta_conv)))
        ) - (Lstar / Cr)

        yc = Rt * math.sqrt(Cr)


        xList.append(xc)
        yList.append(yc)


    # Section 1 -> (convergent to chamber transition)
    if (Cr != 0 and r1 != 0):
        for i in range(N1):
            d_theta = theta_conv / N1

            theta = i * d_theta

            # Points generation
            #
            # Initial point (last chamber point) 
            #
            # Point x: (obtanied by adding the delta x from the 2 curvatures <<from convergent transitions>> and the delta x obtained as 
            # (1 / tan(theta_conv)) * delta y, and where delta y is the convergent section difference in radius 
            #
            x1 = -r2 * Rt * math.sin(math.radians(theta_conv)) - r1 * Rt * math.sin(math.radians(theta_conv)) - (
                (1 / math.tan(math.radians(theta_conv))) * Rt * (math.sqrt(Cr) - 1) - r2 * Rt * (1 - math.cos(math.radians(theta_conv))) - r1 * Rt * (1 - math.cos(math.radians(theta_conv)))
            )
            x = x1 + r1 * Rt * math.sin(math.radians(theta))

            # Point y:
            y = Rt * math.sqrt(Cr) - r1 * Rt * (1 - math.cos(math.radians(theta)))

            xList.append(x)
            yList.append(y)


    # Section 2 -> (throat to convergent transition).
    if (r2 != 0):
        for i in range(N2):
            d_theta = theta_conv / N2

            theta = theta_conv - i * d_theta

            # Points generation
            x = -r2 * Rt * math.sin(math.radians(theta))
            y = Rt + r2 * Rt * (1 - math.cos(math.radians(theta)))

            xList.append(x)
            yList.append(y)

    
    # Section 3 -> (divergent to throat transition)
    if (r3 != 0):
        for i in range(N3):
            d_theta = thetan / N3                   # "theta_final" represented as thetan, this is the angle at which the curvature transitions into the
                                                    # divergent section

            theta = i * d_theta

            # Points generation
            x = r3 * Rt * math.sin(math.radians(theta))
            y = Rt + r3 * Rt * (1 - math.cos(math.radians(theta)))

            xList.append(x)
            yList.append(y)


    # Before Section 4:
    #
    # Divergent section is modeled by a quadratic Bezier curve, with:
    # ->  P0 = Last point of the throat curvature
    # ->  P2 = Exit point
    # ->  P1 = Intersection point between the line from P0 with a thetan angle (rel. to symmetry line) and the line from P2 with a thetae angle (rel. to symmetry line)


    # Point 0 coordinates (Divergent Section Entry)                   
    P0x = xList[-1]
    P0y = yList[-1]

    # Point 2 coordinates (Nozzle Exit)
    P2x = Ln
    P2y = Rt * math.sqrt(eps)

    # The following section is dedicated to calculating point 1's coordinates
    #
    # The gradients of the lines originating from P0 and P2 respectively
    m0 = math.tan(math.radians(thetan))
    m2 = math.tan(math.radians(thetae))

    # The intercepts of the respective lines
    c0 = P0y - m0 * P0x
    c2 = P2y - m2 * P2x

    # Coordinates of Point 1, from the intercepts and gradients of the 2 meeting lines
    P1x = (c2 - c0) / (m0 - m2)
    P1y = (m0 * c2 - m2 * c0) / (m0 - m2)


    # Section 4 -> Divergent section
    if (N4 > 1):
        for i in range(N4):
            t = i / (N4 - 1)

            # Points x and y in terms of parameter t and the coordinates of Points 0, 1 and 2
            x = pow(1-t, 2) * P0x + 2 * t * (1-t) * P1x + pow(t, 2) * P2x
            y = pow(1-t, 2) * P0y + 2 * t * (1-t) * P1y + pow(t, 2) * P2y

            xList.append(x)
            yList.append(y)
    else:
        xList.append(P2x)
        yList.append(P2y)


    return xList, yList



def conicalNozzleGenerator(Rt, N, eps, Cr, Lstar, r1, r2, r3, theta_max):
    # Points lists initializaton
    xList, yList = [], []

    # Nozzle length "Ln"
    Ln = (math.sqrt(eps) - 1) * Rt / math.tan(math.radians(theta_max))                                         # Nozzle length (cm)

    # Convergent section angle (degrees)
    theta_conv = 45

    # Nozzle breakdown : N1 = Number of points in the transition from convergent to chamber (r1)
    #                    N2 = Number of points in the transition from throat to convergent (r2)
    #                    N3 = Number of points in the transition from expansion to throat (r3)
    #                    N4 = Number of points in the expansion section (parabola)

    N1 = int (0.2 * N)
    N2 = int (0.25 * N)
    N3 = int (0.35 * N)
    N4 = N - N1 - N2 - N3

    # Add the injector plate (xc) point, if the user provides the characteristic length, r1 and r2
    if (Lstar != 0 and r1 != 0 and r2 != 0):
        # "x1" (the last chamber point) + the chamber length (Lstar / Cr)
        #
        xc = -r2 * Rt * math.sin(math.radians(theta_conv)) - r1 * Rt * math.sin(math.radians(theta_conv)) - (
            (1 / math.tan(math.radians(theta_conv))) * Rt * (math.sqrt(Cr) - 1) - r2 * Rt * (1 - math.cos(math.radians(theta_conv))) - r1 * Rt * (1 - math.cos(math.radians(theta_conv)))
        ) - (Lstar / Cr)

        yc = Rt * math.sqrt(Cr)


        xList.append(xc)
        yList.append(yc)

    # Section 1 -> (convergent to chamber transition)
    if (r1 != 0):
        for i in range(N1):
            d_theta = theta_conv / N1

            theta = i * d_theta

            # Points generation
            #
            # Initial point (last chamber point) 
            #
            # Point x: (obtanied by adding the delta x from the 2 curvatures <<from convergent transitions>> and the delta x obtained as 
            # (1 / tan(theta_conv)) * delta y, and where delta y is the convergent section difference in radius 
            #
            x1 = -r2 * Rt * math.sin(math.radians(theta_conv)) - r1 * Rt * math.sin(math.radians(theta_conv)) - (
                (1 / math.tan(math.radians(theta_conv))) * Rt * (math.sqrt(Cr) - 1) - r2 * Rt * (1 - math.cos(math.radians(theta_conv))) - r1 * Rt * (1 - math.cos(math.radians(theta_conv)))
            )
            x = x1 + r1 * Rt * math.sin(math.radians(theta))

            # Point y:
            y = Rt * math.sqrt(Cr) - r1 * Rt * (1 - math.cos(math.radians(theta)))

            xList.append(x)
            yList.append(y)


    # Section 2 -> (throat to convergent transition).
    if (r2 != 0):
        for i in range(N2):
            d_theta = theta_conv / N2

            theta = theta_conv - i * d_theta

            # Points generation
            x = -r2 * Rt * math.sin(math.radians(theta))
            y = Rt + r2 * Rt * (1 - math.cos(math.radians(theta)))

            xList.append(x)
            yList.append(y)

    
    # Section 3 -> (divergent to throat transition)
    if (r3 != 0):
        for i in range(N3):
            d_theta = theta_max / N3                   # "theta_final" represented as thetan, this is the angle at which the curvature transitions into the
                                                    # divergent section

            theta = i * d_theta

            # Points generation
            x = r3 * Rt * math.sin(math.radians(theta))
            y = Rt + r3 * Rt * (1 - math.cos(math.radians(theta)))

            xList.append(x)
            yList.append(y)


    # Before Section 4:
    #
    # The initial points for the line (2D nozzle)
    x1, y1 = xList[-1], yList[-1]

    # The interval at which points are analyzed (x-axis)
    dx = (Ln - x1) / (N4 - 1)

    # Section 4 -> Divergent section
    if (N4 > 1):
        for i in range(N4):
            # Points generation
            x = x1 + i * dx
            y = y1 + math.tan(math.radians(theta)) * i * dx


            xList.append(x)
            yList.append(y)
    else:
        xList.append(Ln)
        yList.append(Rt * math.sqrt(eps))


    return xList, yList



