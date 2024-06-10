class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        sum = 0
        step = 0
        for i in range(0, len(nums)):
            for j in range(1, len(nums)):
                print(f"step #{step}")
                sum = nums[i] + nums[j]
                step += 1

                if sum == target:
                    return [i, j]

s = Solution()

nums = [3,3]
target = 6

print(s.twoSum(nums, target))