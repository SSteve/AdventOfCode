using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;

namespace Day9
{
    class Program
    {
        static void Main()
        {
            var test1Values = testData1.Split("\n").Select(n => long.Parse(n)).ToArray();
            Debug.Assert(IsValid(26, 0, 25, test1Values));
            Debug.Assert(IsValid(49, 0, 25, test1Values));
            Debug.Assert(IsValid(100, 0, 25, test1Values) == false);
            Debug.Assert(IsValid(50, 0, 25, test1Values) == false);
            Debug.Assert(IsValid(26, 1, 25, test1Values));
            Debug.Assert(IsValid(65, 1, 25, test1Values) == false);
            Debug.Assert(IsValid(64, 1, 25, test1Values));
            Debug.Assert(IsValid(66, 1, 25, test1Values));

            var test2Values = testData2.Split("\n").Select(n => long.Parse(n)).ToArray();
            var testPart1 = Part1(5, test2Values);
            Debug.Assert(testPart1 == 127);
            var testPart2 = Part2(127, test2Values);
            Debug.Assert(testPart2 == 62, $"Part 2 test is {testPart2}. Should be 62.");

            using var inFile = File.OpenText("../../../../../9.txt");

            var values = inFile.ReadToEnd().Split("\n").Select(val => long.Parse(val)).ToArray();

            var part1Answer = Part1(25, values);
            Console.WriteLine($"Part 1: {part1Answer}");
            var part2Answer = Part2(part1Answer, values);
            Console.WriteLine($"Part 2: {part2Answer}");
            Debug.Assert(part1Answer == 2089807806, $"Part 1 should be 2089807806");
            Debug.Assert(part2Answer == 245848639, $"Part 2 should be 245848639");
        }

        static long Part1(int preambleSize, long[] values)
        {
            foreach (var index in Enumerable.Range(0, values.Count() - preambleSize))
            {
                var targetValue = values[index + preambleSize];
                if (IsValid(targetValue, index, preambleSize, values) == false)
                {
                    return targetValue;
                }
            }
            return -1;
        }

        static long Part2(long targetValue, long[] values)
        {
            foreach (var index in Enumerable.Range(0, values.Count()))
            {
                foreach (var index2 in Enumerable.Range(index + 1, values.Count() - (index + 1)))
                {
                    var rangeSum = values[index..index2].Sum();
                    if (rangeSum == targetValue)
                    {
                        return values[index..index2].Max() + values[index..index2].Min();
                    }
                    if (rangeSum > targetValue)
                    {
                        break;
                    }
                }
            }
            return -1;
        }

        static bool IsValid(long target, int startIndex, int preambleSize, long[] values)
        {
            var xx = values[1..4];
            foreach (var (a, b) in Combinations(values[startIndex .. (startIndex+preambleSize)]))
            {
                if (a + b == target)
                {
                    return true;
                }
            }
            return false;
        }

        /// <summary>
        /// Return each combination of two items from the given list.
        /// </summary>
        /// <param name="values"></param>
        /// <returns></returns>
        static IEnumerable<(long, long)> Combinations(long[] values)
        {
            foreach (var i in Enumerable.Range(0, values.Count()))
            {
                foreach (var j in Enumerable.Range(i + 1, values.Count() - (i + 1)))
                {
                    yield return (values[i], values[j]);
                }
            }
        }

        static string testData1 = @"20
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
1
21
22
23
24
25
45";

        static string testData2 = @"35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576";

    }
}
