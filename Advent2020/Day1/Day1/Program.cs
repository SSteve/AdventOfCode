using System;
using System.Collections.Generic;
using System.IO;

namespace Day1
{
    class Program
    {
        static void Main()
        {
            const string testData = @"1721
979
366
299
675
1456";

            // Test part one.
            const int part1TestCorrectValue = 514579;
            var part1Test = Part1(testData.Split("\n"));
            if (part1Test != part1TestCorrectValue)
                throw new InvalidOperationException($"Part 1 test was {part1Test}. Should be {part1TestCorrectValue}");

            // Test part two.
            const int part2TestTargetValue = 241861950;
            var part2Test = Part2(testData.Split("\n"));
            if (part2Test != part2TestTargetValue)
                throw new InvalidOperationException($"Part 2 test was {part2Test}. Should be {part2TestTargetValue}");

            using var inFile = File.OpenText("../../../../../1.txt");

            var entries = inFile.ReadToEnd().Split("\n");

            var part1Answer = Part1(entries);
            Console.WriteLine($"Part 1: {part1Answer}");

            var part2Answer = Part2(entries);
            Console.WriteLine($"Part 2: {part2Answer}");
        }

        public static int Part1(IEnumerable<string> entryStrings)
        {
            var entries = new List<int>();
            foreach (var entry in entryStrings)
            {
                if (int.TryParse(entry, out var lineValue))
                    entries.Add(lineValue);
            }

            for (int i = 0; i < entries.Count; i++)
            {
                var entry1 = entries[i];
                for (int j = i + 1; j < entries.Count; j++)
                {
                    var entry2 = entries[j];
                    if (entry1 + entry2 == 2020)
                    {
                        return entry1 * entry2;
                    }
                }
            }
            // No solution found.
            return -1;
        }

        public static int Part2(IEnumerable<string> entryStrings)
        {
            var entries = new List<int>();
            foreach (var entry in entryStrings)
            {
                if (int.TryParse(entry, out var lineValue))
                    entries.Add(lineValue);
            }

            for (int i = 0; i < entries.Count; i++)
            {
                var entry1 = entries[i];
                for (int j = i + 1; j < entries.Count; j++)
                {
                    var entry2 = entries[j];
                    for (int k = j + 1; k < entries.Count; k++)
                    {
                        var entry3 = entries[k];
                        if (entry1 + entry2 + entry3 == 2020)
                        {
                            return entry1 * entry2 * entry3;
                        }
                    }
                }
            }
            // No solution found.
            return -1;
        }
    }
}
