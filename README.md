# MetaTarget 1.1

## Features

- 使用异步函数实现并发
- 使用装饰器来进行重试
- 更具体的异常捕，利于后期维护

## 接口监控

|                             SEA                              |                            Swiss                             |                          PassOnline                          |                        Targrt Hunter                         |                          Target Net                          |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| [![sea testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_sea.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_sea.yml) | [![swiss testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_swiss.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_swiss.yml) | [![passOnline testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_passOnline.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_passOnline.yml) | [![targetHunter testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetHunter.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetHunter.yml) | [![targetNet testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetNet.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetNet.yml) |

### PPB2 系列

|                          DNN(ECfp4)                          |                          NB(ECfp4)                           |                     NN(MQN) + NB(ECfp4)                      |                     NN(Xfp) + NB(ECfp4)                      |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| [![ppb2_dnn_ecfp4 testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_dnn_ecfp4.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_dnn_ecfp4.yml) | [![ppb2_nb_ecfp4 testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nb_ecfp4.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nb_ecfp4.yml) | [![ppb2_nnmqn_nbecfp4 testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nnmqn_nbecfp4.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nnmqn_nbecfp4.yml) | [![ppb2_nn_xfp testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_xfp.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_xfp.yml) |
|                  **NN(ECfp4) + NB(ECfp4)**                   |                         **NN(MQN)**                          |                         **NN(Xfp)**                          |                        **NN(ECfp4)**                         |
| [![ppb2_nnnb_ecfp4 testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nnnb_ecfp4.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nnnb_ecfp4.yml) | [![ppb2_nn_mqn testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_mqn.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_mqn.yml) | [![ppb2_nn_xfp testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_xfp.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_xfp.yml) | [![ppb2_nn_xfp testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_xfp.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_nn_xfp.yml) |



## 安装

### 安装依赖

```shell
pip install -r requirements.txt
```

### 安装metaTarget

```shell
python setup.py install
```

## 使用

### 单接口预测

通过调用<code>asyncio</code>运行异步函数

```python
import asyncio
import json

import pandas as pd

from metaTarget import targetNet

if __name__ == "__main__":
    smiles = "FC1=CC=C(CC2=NNC(=O)C3=CC=CC=C23)C=C1C(=O)N1CCN(CC1)C(=O)C1CC1"
    jsonRes = asyncio.run(targetNet(smiles))
    # print(jsonRes)  # 结果为JSON字符串，用json和pandas转换成DataFrame
    res = json.loads(jsonRes)
    out = pd.DataFrame(res).T
    print(out)
```

### 多接口并发

使用<code>asyncio</code>的<code>gather()</code>实现并发

```python
import asyncio
import json

import pandas as pd

from metaTarget import targetNet, passOnline, targetHunter


async def main(smiles):
    return await asyncio.gather(
        targetNet(smiles),
        passOnline(smiles),
        targetHunter(smiles)
    )

if __name__ == "__main__":
    smiles = "FC1=CC=C(CC2=NNC(=O)C3=CC=CC=C23)C=C1C(=O)N1CCN(CC1)C(=O)C1CC1"
    jsonRes = asyncio.run(main(smiles))
    # print(jsonRes)

    res = [json.loads(_) for _ in jsonRes]
    out = [pd.DataFrame(_).T for _ in res]
    # print(out)
```

### 注意

**请勿在Spyder、Jupyter或其他以IPython为运行环境的IDE中直接运行本程序**，否则会抛出以下异常

> RuntimeError: asyncio.run() cannot be called from a running event loop.

这是由于它们已经运行在事件循环（event loop）。

### Spyder

复制代码在IPython中运行

#### Jupyter

将<code>asyncio.run()</code>替换成<code>await</code>关键字

```python
jsonRes = await targetNet(smiles)
```

### Attention

**The exception would be raised while running directly this code in Spyder, Jupyter or other IDE based on  Ipython**.

> RuntimeError: asyncio.run() cannot be called from a running event loop.

Since IPython is already running an event loop, the <code>asyncio.run()</code>should not be instead.

#### Spyder

Paste the code block to Ipython to excute.

#### Jupyter

Use <code>await</code> to instead all <code>asyncio.run()</code>

```python
jsonRes = await targetNet(smiles)
```
