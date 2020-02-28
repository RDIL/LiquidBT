<h1 align="center">Welcome to LiquidBT 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
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

### 🏠 [Homepage](https://docs.rdil.rocks)

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

Copyright © 2019 [Reece Dunham](https://github.com/RDIL).<br />
This project is [GNU General Public License v3](https://gnu.org/licenses/) licensed.

## Monorepo Design

This repository is a monorepo, meaning a lot of packages in one place. Here they all are:

* `liquidbt` - the base of the system
* `liquidbt_i18n` - the package that holds translations for the system
* `liquidbt_plugin_build` - the build plugin
* `liquidbt_plugin_command_clean` - the `clean` command plugin
* `liquidbt_plugin_remove_prints` - a plugin that removes `print()`s from the production source
* `testpackage` - a package used for testing the system
* `unstable` - a collection of packages that don't yet work
  * `liquidbt_plugin_remove_comments` - a plugin that removes comments from the production source
