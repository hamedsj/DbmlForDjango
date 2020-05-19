# DbmlForDjango
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A converter between django models.py and dbml file

## Usage
1. move to django project directory, beside `manage.py` file:
```bash
>>> cd path/to/folder/of/project
```

2. clone DbmlForDjango from github:
```bash
>>> git clone https://github.com/hamedsj/DbmlForDjango
```

3. open django shell:
```bash
>>> python3 manage.py shell
```

4. import modelsToDbml and call convert:
```python
>>> from DbmlForDjango import modelsToDbml as mtd
>>> mtd.convert()
```


5. now you can see `output.dbml` file beside `manage.py` file


## License
Copyright 2020 Shajaravi Hamid-Reza

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
    
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
