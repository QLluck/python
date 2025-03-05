class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        N =  1e4+7 ;
        a = {}
        for i in nums :
            if i not in a :
                a[i]=1
            else :
                a[i]+=1
            
        ans =[];
        for i in range(len(nums)) :
            if (target - nums[i] in a) :
                if(target-nums[i]==nums[i]and a[target-nums[i]]<=1):
                    continue ;
                ans.append(i)
        return ans  

            
