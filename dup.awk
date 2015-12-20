#!/usr/bin/awk -f

#     duptype	id	depth	size	device	inode	priority	name
BEGIN {
	FS="\t"
	OFS="\t"
}

/^#/ {next}

{
	sub(" ","\t")
	sub(" ","\t")
	sub(" ","\t")
	sub(" ","\t")
	sub(" ","\t")
	sub(" ","\t")
	sub(" ","\t")
}

$4<100000 {next}

{
	n = split($8, name, "/")
	id = name[1]
	for(i=2; i<=$3+1; i++)
		id = id "/" name[i]
}

/^DUPTYPE_FIRST_OCCURRENCE/ {
	first = id
	next
}

{print first,id}


## pipe output to ` |sort|uniq -c|sort -n`
