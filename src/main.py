from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.app.config.app_config import settings
from src.app.core.Router import AllRouter

application = FastAPI(
    debug=settings.APP_DEBUG,  #是否开启调试模式
    description=settings.DESCRIPTION, #表示该API文档描述的补充说明，它支持使用Markdown格式来编写
    version=settings.VERSION,  #表示API文档版本号信息
    title=settings.PROJECT_NAME #项目名称
)


#路由
application.include_router(AllRouter)

# 静态资源目录
# application.mount('/', StaticFiles(directory=settings.STATIC_DIR), name="static")
# application.state.views = Jinja2Templates(directory=settings.TEMPLATES_DIR)


#实例化
app = application


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=5001, reload=True)