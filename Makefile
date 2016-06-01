DEPS=lookup.yml lookupold.yml ring0 ring1 ring2 sp2 factory_meta

synclist: $(DEPS)
	./sp2tool.py > tmp && mv tmp synclist

lookup.yml:
	osc cat openSUSE:Leap:42.2 00Meta lookup.yml > tmp && mv tmp lookup.yml

lookupold.yml:
	osc cat openSUSE:Leap:42.1 00Meta lookup.yml > tmp && mv tmp lookupold.yml

ring0:
	osc ls openSUSE:Leap:42.2:Rings:0-Bootstrap > tmp && mv tmp ring0

ring1:
	osc ls openSUSE:Leap:42.2:Rings:1-MinimalX > tmp && mv tmp ring1

ring2:
	osc ls openSUSE:Leap:42.2:Rings:2-TestDVD > tmp && mv tmp ring2

sp2:
	osc ls SUSE:SLE-12-SP2:GA > tmp && mv tmp sp2

factory_meta:
	osc api "/search/package?match=[@project='openSUSE:Factory']" > tmp && mv tmp factory_meta

clean:
	rm -f $(DEPS) synclist
