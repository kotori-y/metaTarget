# MetaTarget 1.1

## Features

- 使用异步函数实现并发
- 使用装饰器来进行重试
- 更具体的异常捕，利于后期维护

## 接口监控

| SEA                                                          | Swiss TargetPrediction                                       | PassOnline                                                   | Targrt Hunter                                                | Target Net                                                   | PPB2                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| [![sea testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_sea.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_sea.yml) | [![swiss testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_swiss.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_swiss.yml) | [![passOnline testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_passOnline.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_passOnline.yml) | [![targetHunter testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetHunter.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetHunter.yml)c | [![targetNet testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetNet.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_targetNet.yml) | [![ppb2_dnn_ecfp4 testing](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_dnn_ecfp4.yml/badge.svg)](https://github.com/kotori-y/metaTarget/actions/workflows/test_ppb2_dnn_ecfp4.yml) |

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

