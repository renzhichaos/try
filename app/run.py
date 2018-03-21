import app.jdsign as jd

# 自动登录 + 领京豆 + 申请试用
jd.get_activity_ids(1, 2, 1, "1", "jd账号", "jd密码")
jd.get_activity_ids(1, 2, 1, "3", "jd账号", "jd密码")
jd.close()
