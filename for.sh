#!/bin/bash
        for i in $( ls *vcf ); do
            echo item: $i
	    bgzip $i
	    tabix -f -p vcf $i.gz
        done
