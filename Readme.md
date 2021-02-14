# Yurlungur

|       | Windows | Linux/macOS | code |
| ----- | ------ | --- | --- |
| OS | [![Build status](https://ci.appveyor.com/api/projects/status/46vinb8jd1jbbhdg?svg=true)](https://ci.appveyor.com/project/sho7noka/yurlungur) | [![Build Status](https://travis-ci.org/sho7noka/Yurlungur.svg?branch=dev)](https://travis-ci.org/sho7noka/Yurlungur) | [![Latest PyPI version](https://img.shields.io/pypi/v/yurlungur.svg)](https://pypi.python.org/pypi/yurlungur) |


The universal scripting environment with Python which Maya, Houdini and Unreal Engine.

## summary
DCC tool scripting is almost used Python, but these api isn't similarly anything.
If you make lightweight tool, need to remember each application manners.
Yurlungur is common interface which adapted each application for universal wrapper.

Yurlungur is inspired by [PyMEL](https://github.com/LumaPictures/pymel).

### future
Yurlungur is pure Python and can be used **synchronously** in mixed Python2 and Python3 environments with RPC.

* Houdini Object Model like command wrapper.
* Qt for Python shorten accessor.
* Useful snippets for Game&VFX technical artist.

### available
|       | Node | Attribute | Sync |
| ---- | --- | --- | --- |
| Maya (2016~) | ○ | ○ | ○ |
| Substance (2018.1.2~) | ○ | ○ | ☓ |
| Houdini (16~) | ○ | ○ | ☓ |
| Blender (2.80~) | ○ | ○ | ○ |
| Unreal Engine (4.22~) | ○ | ○ | ☓ |
| Unity (2019.1~) | ○ | ○ | ○ |
| Nuke (10~) | ○ | ○ | ☓ |
| Cinema4D (R21~) | ○ | ○ | ☓ |
| Davinci Resolve(&Fusion) (15~) | ○ | ○ | ☓ |
| Marmoset Toolbag (3~) | ○ | ○ | ☓ |
| RUMBA | ○ | ○ | ☓ |

We also support 3dsMax and Photoshop.

### Installation
```bash
$ pip install yurlungur
```

#### optional
If you use UE4 Editor or Standalone for full supports, Yurlungur recommend `Qt for Python` module.

```bash
$ pip install PySide2
```

### semantics

```python
# Blender Python
import bpy
bpy.data.objects["foo"].bar = True
```

```sh
// Maya MEL
setAttr "foo.bar" true;
```

```cs
// Unity C#
using UnityEngine;
UnityEngine.GameObject.Find("foo").bar = true;
```

YNode behaves as a base class for the object.

```python
# yurlungur
import yurlungur as yr

yr.Node("foo").bar.set(True)
``` 

[sample script](./CONTRIBUTING.md).

## contribution

lets see [CONTRIBUTING](./CONTRIBUTING.md).

## License

Yurlungur is [MIT](./LICENSE.md) License.
