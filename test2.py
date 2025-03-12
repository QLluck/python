class Solution:
    def addDigits(self, num: int) -> int:
        ans= 0 ; 
        def f(n):
            ans = 0 ;
            while n:
                ans += n%10
                n//=10;
            return ans
        ans = f(num);
        while ans >=10:
            ans = f(ans);
        return ans;
a = Solution()
for i in range(1000):
      print(i,a.addDigits(i));