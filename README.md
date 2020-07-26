<h1 align="center">Welcome to LiquidBT 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/pypi/v/liquidbt" />
  <a href="https://docs.rdil.rocks" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="https://gnu.org/licenses/" target="_blank">
    <img alt="License: GNU General Public License v3" src="https://img.shields.io/badge/License-GNU General Public License v3-yellow.svg" />
  </a>
  <a href="https://twitter.com/rdil_pickle" target="_blank">
    <img alt="Twitter: rdil_pickle" src="https://img.shields.io/twitter/follow/rdil_pickle.svg?style=social" />
  </a>
</p>

> LiquidBT is a tool for managing the full lifecycles of Python packages.
> Build, test, deploy, and more all in the same place.

### 🏠 [Homepage](https://docs.rdil.rocks/libraries/liquidbt/)

## Install

```sh
pip install liquidbt
```

## Author

👤 **Reece Dunham**

* Website: https://rdil.rocks/
* Twitter: [@rdil_pickle](https://twitter.com/rdil_pickle)
* GitHub: [@RDIL](https://github.com/RDIL)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!
Feel free to check the [issues page](https://github.com/RDIL/liquidbt).
You can also take a look at the [contributing guide](https://docs.rdil.rocks).

## ❤️ Show your support

Please give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [Reece Dunham](https://github.com/RDIL).

This project is [GNU General Public License v3](https://gnu.org/licenses/) licensed.

## Monorepo Design

This repository is a monorepo, meaning a lot of packages in one place. Here they all are:

* `liquidbt` - the base of the system
* `liquidbt_plugin_command_clean` - the `clean` command plugin
* `liquidbt_plugin_deploy` - the deploy plugin
* `liquidbt_plugin_remove_prints` - a plugin that removes `print()`s from the production source
* `testpackage` - a package used for testing the system
* `unstable` - a collection of packages that don't yet work
