#!/usr/bin/env python3
# queue_timings.py
# Analysis script for bodyfetcher queue timings. Call from the command line using Python 3.

import os.path
# noinspection PyPep8Naming
import bisect
import math


def main():
    if os.path.isfile("bodyfetcherQueueTimings.csv"):
        queue_data = {}
        try:
            with open("bodyfetcherQueueTimings.csv", "r") as f:
                for line in f:
                    site, timing = line.rstrip().split(",")
                    timing = float(timing)  # TODO: Find out actual type
                    if site in queue_data:
                        bisect.insort(queue_data[site], timing)
                    else:
                        queue_data[site] = [timing]
        except ValueError:  # Too many values to unpack
            print("That data doesn't look valid...")
        # TODO: EOFError?

        print("SITE,MIN,MAX,AVG,Q1,MEDIAN,Q3,STDDEV,COUNT,98P_MIN,98P_MAX")
        # noinspection PyUnboundLocalVariable
        for site, times in queue_data.items():
            median = times[int(len(times) * 0.5)]
            q1 = times[int(len(times) * 0.25)]
            q3 = times[int(len(times) * 0.75)]

            mean = sum(times) / len(times)
            diff_sqr = [(x - mean) ** 2 for x in times]
            stddev = math.sqrt(sum(diff_sqr) / len(diff_sqr))

            min98 = max(mean - 2 * stddev, min(times))
            max98 = min(mean + 2 * stddev, max(times))

            print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}"
                  .format(site.split(".")[0], min(times), max(times), mean, q1, median,
                          q3, stddev, len(times), min98, max98))

    else:
        print("bodyfetcherQueueTimings.csv doesn't exist. No data to analyse. Have you enabled queue timing logging?")


if __name__ == "__main__":
    main()
