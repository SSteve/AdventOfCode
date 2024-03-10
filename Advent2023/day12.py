"""
https://www.reddit.com/r/adventofcode/comments/18ghux0/2023_day_12_no_idea_how_to_start_with_this_puzzle/
if it starts with a ., discard the . and recursively check again.

if it starts with a ?, replace the ? with a . and recursively check again, AND replace it with a # and recursively check again.

it it starts with a #, check if it is long enough for the first group, check if all characters in the first [grouplength] characters are not '.', and then remove the first [grouplength] chars and the first group number, recursively check again.

at some point you will get to the point of having an empty string and more groups to do - that is a zero. or you have an empty string with zero gropus to do - that is a one.

there are more rules to check than these few, which are up to you to find. but this is a way to work out the solution.
"""
