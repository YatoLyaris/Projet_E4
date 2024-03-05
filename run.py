import subprocess

def main():
    subprocess.run(["python", ".\identification\points.py"])
    subprocess.run(["python", ".\modelisation\Plant_2to3.py"])
    subprocess.run(["python", ".\interface\stl_interf.py"])

main()