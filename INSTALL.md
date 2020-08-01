### 初始化环境
```
virtualenv --no-site-packages venv
python -m ipykernel install --user --name venv --display-name  venv_a1chemy
```

## 注意事项
1. ipykernel 新建一个虚拟环境的内核, 并且让jupyter启动的时候指向这个内核
2. matplotlib
    - pip install matplotlib==3.2.2 目前最新版本有bug(傻逼社区, 这都能出来?)
    - 注意安装一些额外的包: ipympl
    - pip install widgetsnbextension 展示的时候需要的插件
    - 目前对jupyter lab支持的不是特别好, 继续使用notebook