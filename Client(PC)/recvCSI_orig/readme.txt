 the gived compiled bin is not the same as you directly maked.

 the gived bin don't have this output of endian_flag.This bit is at the start of the file. the matlab script is not designed to process this bit.So, this output will destroy the while structure and the matlab script could not read the file which has the endian_flag output.

this problem confused me a whole day

solution:
	remove fwrite(&endian_flag,1,1,fp); 

after that, the compiled bin could output the file with the same structure as the gived bin.
