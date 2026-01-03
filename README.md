# Hova

![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue)
![GitHub Repo stars](https://img.shields.io/github/stars/G4brielXavier/HovaForge?style=social)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/G4brielXavier/HovaForge)
![GitHub all releases](https://img.shields.io/github/downloads/G4brielXavier/HovaForge/total)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgrey)
![Issues](https://img.shields.io/badge/Issues-welcome-brightgreen)

![HOVA](./assets/HOVA.png)

## Summary

- [Hova](#hova)
  - [Summary](#summary)
  - [What's Hova?](#whats-hova)
  - [Why Hova Exists](#why-hova-exists)
  - [Who is Hova for?](#who-is-hova-for)
  - [Philosophy](#philosophy)
  - [Examples](#examples)
  - [Core Concepts](#core-concepts)
  - [Hova Roadmap](#hova-roadmap)
  - [How to Install Hova?](#how-to-install-hova)
      - [1. Install on Website](#1-install-on-website)
      - [2. Install with `pip`](#2-install-with-pip)
      - [3. Install on Releases](#3-install-on-releases)
  - [Hova Quick Use (3 steps to learn Hova now)](#hova-quick-use-3-steps-to-learn-hova-now)
  - [JSON, YAML or TOML conversion](#json-yaml-or-toml-conversion)
  - [License](#license)
  - [Support the project?](#support-the-project)
  - [How to Contribute?](#how-to-contribute)

Stop writing repetitive JSON and YAML by hand.
Hova is a human-friendly DSL that lets you structure worlds, entities and data — then instantly export them to JSON, YAML or TOML.

![HovaCode](./assets/HovaCoding.gif)

## What's Hova?

Hova is a Domain-Specific Language designed to describe and organize entities in a clean, readable and structured way.
It lets you define your data once and automatically export it as JSON, YAML or TOML.

If you want know more, visit the documentation: https://hova.space

## Why Hova Exists

Hova was created by a *brazilian called Gabriel Xavier (dotxavierket)* to speed up world-building and entity-driven projects such as games, books, characters and more.
Instead of writing repetitive JSON or YAML by hand, Hova gives you a clean syntax and integrated helpers to keep everything organized.

## Who is Hova for?

Hova is great for:
- Game Developers
- World builders
- Config-heavy systems
- Modding tools
- Narrative engines
- Structured content creators

## Philosophy

*Hova is not a programming language.* <br>
*It does not execute logic.* <br>
*It exists only to describe structured data in the cleanest way possible.*

## Examples

For the first example, I will show a simple structure to manage several enemies in a game.

```hova
anvil Enemies be

    atomic be
        atom creator : "GabrielXavier"
        atom emit : "json"
    end

    ore Slime be
        spark Damage int : 15
        spark MaxLife int : 50
    end

    ore KnightGuard be
        spark Damage int : 23
        spark MaxLife int : 200
    end

end
```

In this example, we created an `anvil` called **Enemies**.
The `anvil` is the root scope that contains everything inside it.

I put `atomic` that represents the `anvil` metadata, and two `ore`'s that are entities with propert that are represented as `spark`.

If you see the `atomic`, you will find `atom emit : "json"`, that mean when execute `hova forge file.hova` in CLI, this Hova code will convert to a json file. This **Hova** code will stay like this when convert to json.

```json
{
    "Enemies": {
        "atomic": {
            "config": {},
            "creator": "GabrielXavier",
            "emit": "json"
        },
        "ores": {
            "Slime": {
                "sparks": {
                    "Damage": {
                        "type": "IntegerLiteral",
                        "value": 15
                    },
                    "MaxLife": {
                        "type": "IntegerLiteral",
                        "value": 50
                    }
                }
            },
            "KnightGuard": {
                "sparks": {
                    "Damage": {
                        "type": "IntegerLiteral",
                        "value": 23
                    },
                    "MaxLife": {
                        "type": "IntegerLiteral",
                        "value": 200
                    }
                }
            }
        }
    }
}
```

You can remove somethings on output using **HovaATOM's**

```json
{
    "Enemies": {
        "atomic": {
            "config": {
                "hova.definer.types": "off",
                "hova.encompass.directSparks": "on",
                "hova.encompass.directOres": "on"
            },
            "creator": "GabrielXavier",
            "emit": "json"
        },
        "Slime": {
            "Damage": 15,
            "MaxLife": 50
        },
        "KnightGuard": {
            "Damage": 23,
            "MaxLife": 200
        }
    }
}
```

Or let it more MINIMAL.

```json
{
    "Enemies": {
        "Slime": {
            "Damage": 15,
            "MaxLife": 50
        },
        "KnightGuard": {
            "Damage": 23,
            "MaxLife": 200
        }
    }
}
```

## Core Concepts

- `anvil` -> root container / world
- `atomic` -> metadata + output behaviour
- `ore` -> entity / object
- `spark` -> property / field of entity
- `seal` -> entity behaviour
- `rune` -> reusable / alias
- `temper` -> contract / field pattern of entity


## Hova Roadmap

Soon (its not guaranteed): 
- Conversions to **Markdown** and **.ini** file type
- Hova IDE
- VsCode Plugin 
- Better tooling

More informations: [Hova - Roadmap](./Hova%20–%20Roadmap%20Oficial.md)

## How to Install Hova?


#### 1. Install on Website

1. To install, go to Official Hova Website in https://hovaforge.xyz.
2. After, click in the 'Download' button
3. Open *HovaTools.exe* installer downloaded
4. Next, Next and Install
5. And that's it!

To test if Hova works

1. Open the terminal (CTRL+R and type 'cmd' or 'wt')
2. Test using `hova --version`. It will show the current hova version


#### 2. Install with `pip`

1. Open your terminal and use:
    ```
    pip install hova
    ```

2. After, test if works with:
    ```
    hova --version
    ```

#### 3. Install on Releases

1. Go to *Releases*
2. Install "*hova-installer-x.x.x.exe*"
3. Open the installer
4. Follow the instructions


## Hova Quick Use (3 steps to learn Hova now)

1. Create a file `shapes.hova` (or with another name)
2. Write the code or copy and paste it below
    ```hova
        anvil shapes be

            atomic be
                atom emit : "json"
                atom creator : "dotxav"
            end
    
            ore Square be
                spark sides int : 4
            end

            ore Triangle be
                spark sides int : 3
            end

            ore Circle be
                spark sides int : null
            end
    
        end
    ```
3. Open the terminal and use `hova forge shapes.hova`.

Okay, now the `shapes.hova` will become `shapes.json` in `.\outHova\Json`

Feel free to use your creativity to create anything you want with Hova, it's very important.*



## JSON, YAML or TOML conversion

The conversions are what makes Hova useful.

The setup of file type conversion is defined in the `atomic`.

```hova
anvil YourWorld by You be

    atomic be
        atom emit : "yaml" .. here
    end

end
```

*In this current version you can convert to **JSON**, **YAML**, or **TOML***. Soon new convertions will be support.

When is used `hova forge filename.hova`, the system will create a folder called `outHova` and inside, another folder that represent file type (for example: a folder `/Json` to json files).

```yaml
outHova/
    Json/
        json files here
    Yaml/
        yaml files here
    Toml/
        toml files here
```

## License

Hova is offered under a **dual license**:

- **Community License** — Free for individuals, students, hobby projects, open-source usage, research and non-profit.
- **Commercial License** — Required for companies, organizations, SaaS platforms, or any commercial/enterprise usage.

See:

- [LICENSE-Community.md](./LICENSE-Community.md)
- [LICENSE-Commercial.md](./LICENSE-Commercial.md)

For commercial inquiries, email: dotxavket@gmail.com

*If you're a company using Hova in production or commercial products, you need a commercial license.*


## Support the project?

Hova is an indie project.

If Hova helped you build, organize or speed up your projects, consider supporting the project!

Supporting the project helps development continue and allows new features to be released faster.

- 💲 Pix (BR) — E-mail: nopaxxff@gmail.com <br>
Foreigners can donate via Wise using this *Pix*.

## How to Contribute?

1. Fork this repository  
2. Create a new branch (`git checkout -b feature/amazing-feature`)  
3. Commit your changes (`git commit -m 'Add amazing feature'`)  
4. Push the branch (`git push origin feature/amazing-feature`)  
5. Open a Pull Request  

All contributions are welcome — fixes, ideas, examples, docs, everything!

