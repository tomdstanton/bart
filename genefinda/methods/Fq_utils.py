import mmap
import re
import contextlib
import io
import gzip

class FqUtils():

    in_ = 'test/test_R1.fastq.gz'
    
    def try_open(in_):
        fp = None
        try:
            import gzip
            fp = gzip.open(reads_file)
            ln = fp.read(2)  # read arbitrary bytes to check if gzipped
            fp.close()  # if we're here, it's definitely gzip
            fp = gzip.open(reads_file)
        except Exception as e:
            if fp: fp.close()
            fp = open(reads_file)
        return fp

    # auxiliary function
    def get_read_length(list_reads):
        read_lengths = []
        for reads_file in list_reads:
            fp = try_open(reads_file)
            # read the 1000 first reads
            from methods.readfq import readfq
            read_count = 0
            for name, seq, qual in readfq(fp):
                read_count += 1
                read_lengths += [len(seq)]
                if read_count > 999:
                    break
            fp.close()

        # so, on CEA cluster, loading numpy forced minia to run on a single thread.
        # so let's not use numpy here. days of debugging to get that.
        import math
        def percentile(data, percentile):
            size = len(data)
            return sorted(data)[int(math.ceil((size * percentile) / 100)) - 1]

        if len(read_lengths) == 0:
            print("Warning: couldn't detect max read length. Are you sure the input is correct?")
            exit("")

        estimated_max_read_length = percentile(read_lengths, 90)
        print("Setting maximum kmer length to: " + str(
            estimated_max_read_length) + " bp")  # based on the 90 percentile of 1000 first reads lengths of each input file
        return estimated_max_read_length

    #def gc_calc(self):

    def grep(pattern, file_path):
        with io.open(file_path, "r", encoding="utf-8") as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
                for match in pattern.findall(m):
                    return(print(match))

    grep(re.compile(b'@'), test)

    with io.open(in_, "r", encoding="utf-8") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            for line in m:
                print(len(line))



handle = open(in_, "rb")
mapped = mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ)
gzfile = gzip.GzipFile(mode="r", fileobj=mapped)
print(gzfile.read())