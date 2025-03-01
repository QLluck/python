#自定义函数
def file_read(s):
    
    try:
        f = open(s,"r");
        print( f.read());
    except Exception as e :
        print(f"出现错误{e}")
    else:
        f.close()
        

        
    
