import psutil as ps

for proc in ps.process_iter():
    try:
        flist = proc.open_files()
        if flist:
            print(proc.pid, proc.name)
            for nt in flist:
                print("\t", nt.path)
    except ps.NoSuchProcess as err:
        print("*****", err)
