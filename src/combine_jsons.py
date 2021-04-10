


if __name__ == "__main__":
    pref = 'D:\\Projects\\gitscraper\\resources\\ResultingJSON\\Java\\'
    out_file = 'D:\\Projects\\gitscraper\\resources\\ResultingJSON\\Java\\final_code.json'
    filenames = [pref+'code.json', pref+'code2.json', pref+'code3.json',pref+'code4.json']
    count = 0;
    with open(out_file, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
                    count += 1

    print(count)