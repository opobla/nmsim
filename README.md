# nmsim
Neutron Monitor Simulator

El objetivo de este software es el de simular el comportamiento de un monitor de neutrones ideal, compuesto por 18 contadores, en el que los eventos que provocan la llegada de los neutrones están espaciados en el tiempo según una distribución aleatoria exponencial.

## Instalación

```bash
virtualenv venv --python=python3
pip install -r requirements.txt
```

## Ejecución del código

Activar el entorno virtual `source venv/bin/activate` y ejecutar el código haciendo:

```bash
python nm-sim/run.py | head
     0      0 [0x00000000]     0.006869s - 100000000000000000 [0x020000]
    44     44 [0x0000002c]     0.006891s - 000000000000000000 [0x000000]
  6792   6836 [0x00001ab4]     0.010286s - 000000000000000010 [0x000002]
    45   6881 [0x00001ae1]     0.010308s - 000000000000000000 [0x000000]
  4060  10941 [0x00002abd]     0.012338s - 000000000000010000 [0x000010]
    45  10986 [0x00002aea]     0.012360s - 000000000000000000 [0x000000]
   153  11139 [0x00002b83]     0.012436s - 010000000000000000 [0x010000]
    45  11184 [0x00002bb0]     0.012458s - 000000000000000000 [0x000000]
  4699  15883 [0x00003e0b]     0.014808s - 000000000000000010 [0x000002]
    44  15927 [0x00003e37]     0.014830s - 000000000000000000 [0x000000]
```

Cada una de las columnas, de izquierda a derecha, muestra:
* Delta: el tiempo transcurrido desde el último evento expresados en steps (cada step son 500ns)
* Global counter: contador global (timestamp) en steps
* Contador global expresado en 32bits
* Tiempo general de simulación en segundos
* Estado de la salida de cada uno de los contadores
* Estado de la salida de cada uno de los contadores expresado con tres bytes en hexadecimal
