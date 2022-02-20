def verifiy_pk(pk):
    if not pk:
        return False
    else:
        try:
            int(pk)
        except ValueError:
            return False
        return pk