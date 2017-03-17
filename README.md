相信对 NBA 感兴趣的大兄弟一定不会对球星卡陌生吧，虽然不知道咱们这个圈子对 NBA 感兴趣的大兄弟多不多。但是，不感兴趣也问题不大，本文阐述的方法其实是通用的图片合成方法。

让我们来看一张球星卡：

![](https://dn-mhke0kuv.qbox.me/c1bd4e1cc1471ae6403f.png)

这种球星卡可以划分为5个部分
1.  球员动作图
2.  球员姓名
3.  球队logo
4.  底板背景图
5.  装饰边框图

今天我们要干的事情就是找到这5个素材然后用 Python 把他们组合起来，那么这个时候肯定有大兄弟会有疑问了，直接用 PS 套起来不就好了吗，讲道理这样做确实方便快捷，但是前提是你只做这一张卡，当你要为联盟大概450名球员制作球星卡的时候，你就需要一个脚本来帮助你完成了（对 PS 不太熟，如果 PS 也可以，可以告诉我哈）。

这篇文章需要一点 Python 基础，完全不了解 Python 的大兄弟最好去学习一点基础知识再看。

OK 让我们开始吧！

### 准备素材

就像开头提到的，我们需要5种素材。这5种素材我都会提供若干个给大家练手。

![](https://dn-mhke0kuv.qbox.me/ba1fe7abdeead6a8895c.png)

上面的图片实际上只有4个素材，还有一个就是球员的名字了，球员的名字我们可以在组合过程中使用 ImageDraw 和 ImageFont 加载球员姓名。

为了避免字体路径和中文乱码的问题，我还提供了一个微软雅黑的字体。

素材可以在 [**这里**](https://www.github.com/XatMassacrE/compose_nba_trading_cards) clone 或者下载，声明：本文所有涉及的素材和图片仅供交流学习使用。

### 开始写代码

我们的场景是为联盟中的所有球员制作球星卡，那么所有的球员自然是从数据库里面查出来的了，这里为了练习，我们可以 mock 一些数据（虽然，讲道理，波什并不能放在 SUPER 里面，但是这里只有一张装饰边框图，所以就勉为其难的和吾皇放在一个等级了）。

```
mock_data = [
    {
        'id': 1966,
        'cn_name': '勒布朗-詹姆斯',
        'team_id': 5,
        'category': 'SUPER'
    },
    {
        'id': 1977,
        'cn_name': '克里斯-波什',
        'team_id': 14,
        'category': 'SUPER'
    }
]
```

有数据之后，我们就来遍历这些球员，找到我们需要的属性，再传入到一个组合函数中。

```
def compose_all(all):
    for player in all:
        id = player['id']
        # if id == 1966:
        if True:
            category = player['category']
            player_img =  str(id) + '.png'

            team_id = player['team_id']
            team_img = str(team_id) + '.png'
            name = player['cn_name']
            category = player_category.index(category) + 1
            category_img = 'card_bg_' + str(category) + '.png'

            output_name = str(id) + '.png'
            print('start compose ' + str(id))
            compose(player_img, name, team_img, category_img, output_name)
```

这里有个个人习惯，因为经常在服务器上写一些脚本，所有`if True:`那个地方就是调试用的，当一个球员调试没问题之后，注释掉，跑代码，这样可以不用再调整缩进了，不知道其他的大兄弟这个地方喜欢怎么写。

在这里我默认会对球员分档（根据一些数据信息）

```
player_category = ["SUPER", "CORE", "BLUE", "SIX", "BENCH"]
```

对应档位的装饰边框分别为`card_bg_1.png`，`card_bg_2.png`等。
检查5个素材是否都拿到了：

1.  球员动作图 -> player_img
2.  球员姓名 -> name
3.  球队logo -> team_img
4.  底板背景图 —> ** None **
5.  装饰边框图 -> card\_bg\_n.png (n 对应档位）

还差一个底板背景图，因为每个球员底板背景图都一样，所以在组合函数中直接使用就好了。

在我们去组合球星卡之前，还有一个问题需要解决，那就是我们不能保证所有素材都在同一个目录下，那么我们就需要给每个素材指定一个目录，这样我们在组合球星卡的时候就可以一马平川了。

```
team_path = './logo/'
player_path = './player_img/'
output_path = './trading_cards/'
font_file = './assets/msyh.ttf'
card_decorate_path = './assets/'
```

设置好路径之后写上我们的组合函数，为了保证这个函数的正常运行，我们需要导入三个模块。
```
import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw
```
如果提示没有找到模块，请使用下面的命令进行安装

```
pip install Pillow
pip install numpy
```
Pillow 关于图片处理的详细文档请参考 [**Pillow**](https://github.com/python-pillow/Pillow)

下面是我们的组合函数
```
def compose(player_img, name, team_logo, category_img, output_name):

    card_bg = card_decorate_path + 'bg.png'
    player_img_offset_height = 15

    if not os.path.isfile(player_path + player_img):
        need_manual_compose.append(player_img)
        print(player_path + player_img + ' is not exist')
        return

    player_img = Image.open(player_path + player_img).convert('RGBA')
    bg_img = Image.open(card_decorate_path + category_img).convert('RGBA')
    card_bg_img = Image.open(card_bg).convert('RGBA')
    logo = Image.open(team_path + team_logo).convert('RGBA')

    logo = logo.resize((100,100), Image.ANTIALIAS)

    card_bg_img.paste(player_img, (35,player_img_offset_height), player_img)
    card_bg_img.paste(bg_img, (0,0), bg_img)
    card_bg_img.paste(logo, (95,315), logo)

    font = ImageFont.truetype(font_file, 20)
    d = ImageDraw.Draw(card_bg_img)

    try:
        name = unicode(name, 'utf-8')
    except NameError:
        name = name
    d.text((12, 12), name, font=font, fill=(255,255,255))

    card_bg_img.save(output_path + output_name, quality=100)
```

有几个问题需要说明一下：
1.  有些球星动作的素材可能找不到，那么就将找不到的球员记录下来，最后手工处理。
2.  因为我们要使用到 alpha 通道，所以需要 convert('RGBA')
3.  在图片 paste 之前必须保证团片和粘贴范围像素一样，不一样的话就使用 resize 函数变成一样的，Image.ANTIALIAS 参数的作用是抗锯齿，这样 resize 出来的图片边缘会更圆润。
4.  b 图片贴在 a 图片上，使用 a.paste(b, (x,y), b)，(x,y) 为左上角的坐标，第三个参数 b 是作为 mask，如果不使用这个参数会导致 b 图片透明的部分也覆盖在 a 上面。
5.  这个程序在 python2 和 python3 上都可以运行。

OK，让我们来看一看结果怎么样吧

![](https://dn-mhke0kuv.qbox.me/a4374ac6586c53df0fb4.png)

恩，似乎还不错，但是大家会发现波什的手没了，所以说一马平川什么的都是骗人的。

经过我个人的观察，会发现大部分的球星动作图都是和詹姆斯类似的（即球员的动作在图片中的位置是靠下的），如果下移粘贴坐标会导致球星卡的主要局域出现大面积的空白。一计不成，再生一计，我们可以对类似波什的动作图做特殊处理，下移他们的粘贴坐标就可以了。

ok，问题来了，人眼一看就会知道哪个动作图高哪个动作图低，那么 Python 怎么才能知道呢？

![](https://dn-mhke0kuv.qbox.me/fe6f118a9dbbb82fc434)

可以看到，每张动作图的大小是一样的，但是具体的动作在图片中的分布是不一样的。

这个时候我们就需要`numpy`这个库来帮助我们把图片转换成像素矩阵，然后我们对矩阵进行逐行扫描并记录有效像素出现的位置，这样就可以判断哪些动作图是偏高的。

```
def calculateUsefulHeight(img):
    img = Image.open(player_path + img).convert('RGBA')
    w, h = img.size
    mat = np.array(img)

    for i in range(mat.shape[0]):
        if not allEqual(mat[i]):
            return h - i

def allEqual(line):
    w = len(line)
    if not w:
        return True
    init_value = line[0][3]
    step = 10
    for i in range(int(round(w/step))):
        if line[i * step][3] == init_value:
            continue
        else:
            return False
    return True
```

然后再在组合函数中加入对动作图高的特殊处理的代码就可以了。

```
def compose(player_img, name, team_logo, category_img, output_name):
    ...
    # deal with high player image
    h = calculateUsefulHeight(player_img)
    # 这个地方的310是球星卡展示球员动作的最大高度
    if h > 310:
        offset = h - 310
        player_img_offset_height += offset
```

再来跑一遍，看看效果如何。

![](https://dn-mhke0kuv.qbox.me/ef90a80aec3fda536529)

不错，这样就可以了，尤其是一瞬间跑出来 450 张看起来效果还不错的球星卡还是非常的爽的。

OK了，到这里应该就可以结束了，源码可以在  [**这里**](https://www.github.com/XatMassacrE/compose_nba_trading_cards) 得到，里面包含本文所有涉及的图片，素材和代码。

如果各位大兄弟，有更好的设计和布局也欢迎和我交流。
