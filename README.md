# pyls2

A simple program to illustrate iterative development for COMP350.

[Link to video](https://drive.google.com/file/d/1Zzlg2fzZlPV1G-knN9CdlIzseRlGC_GE/view?usp=drive_link)

The ask is to develop a simplified version of the `ls` program.
The script is expected to be run in the following ways --

## Help

```
> pyls -h 
or
> pyls --help
```

## Basic usage

Lists current directory

```
>  pyls
file1.txt
file2.pdf
dir3
dir4
```

## Show file type

```
>  pyls -F
file1.txt
file2.pdf
dir3/
dir4/
script10*
file109.py
```

## Long format display

```
> pyls -l
2024-04-12 16:04:23   2454  file1.txt
2023-05-25 07:37:56   1712  file2.txt
2024-06-20 01:23:12      0  dir3
2022-05-19 15:31:43      0  dir4
2023-04-16 19:51:45   4876  script10
2024-06-30 21:07:22  93487  file109.py
```
