include ../config.mk
PLAF = -DLOGICAL_PROCESSORS=$(maxthreads_powerof2) -DMAX_TID_POW2=$(maxthreads_powerof2) -DCPU_FREQ_GHZ=$(cpu_freq_ghz) -DCPU_FREQ=$(cpu_freq_ghz)

GPP = g++
FLAGS = -std=c++11 -mcx16 
FLAGS += -O2
# FLAGS += -O0 -fsanitize=address -static-libasan -fsanitize=leak
FLAGS += -g
FLAGS += -DNDEBUG
FLAGS += $(PLAF)
FLAGS += -DUSE_GSTATS
#FLAGS += -DNO_FREE
#FLAGS += -DUSE_STL_HASHLIST
FLAGS += -DUSE_SIMPLIFIED_HASHLIST
#FLAGS += -DRAPID_RECLAMATION
#FLAGS += -DRWLOCK_PTHREADS
#FLAGS += -DRWLOCK_FAVOR_WRITERS
FLAGS += -DRWLOCK_FAVOR_READERS
#FLAGS += -DRWLOCK_COHORT_FAVOR_WRITERS
#FLAGS += -DSNAPCOLLECTOR_PRINT_RQS
#FLAGS += -DUSE_RQ_DEBUGGING -DRQ_VALIDATION
#FLAGS += -DRQ_VISITED_IN_BAGS_HISTOGRAM
#FLAGS += -DRQ_HISTOGRAM
#FLAGS += -DADD_DELAY_BEFORE_DTIME
#FLAGS += -DRQ_LOCKFREE_WAITS_FOR_DTIME
#FLAGS += -DUSE_DEBUGCOUNTERS
#FLAGS += -DBLOCKBAG_ITERATOR_COUNT_BLOCKS_TRAVERSED
#FLAGS += -DDEBUG=if\(1\) -DDEBUG1=if\(1\) -DDEBUG2=if\(1\)
#FLAGS += -DDEBUG=if\(1\) -DDEBUG1=if\(0\) -DDEBUG2=if\(0\)
FLAGS += -DDEBUG=if\(0\) -DDEBUG1=if\(0\) -DDEBUG2=if\(0\)
FLAGS += -DMEMORY_STATS=if\(1\) -DMEMORY_STATS2=if\(1\)
#FLAGS += -DMEMORY_STATS=if\(0\) -DMEMORY_STATS2=if\(0\)
FLAGS += -DINSERT_FUNC=insertIfAbsent
#FLAGS += -DUSE_PAPI
# FLAGS += -DUSE_TRACE

# FLAGS += -DDEBRA_DISABLE_READONLY_OPT
#FLAGS += -DEERPRCU_DISABLE_RDTSC_TTAS
# FLAGS += -DSKIPLIST_DEBUGGING_FLATTEN_MAX_LEVEL

# Include bundle configuration macros
include bundle.mk

LDFLAGS = -L../lib
LDFLAGS += -I../
LDFLAGS += -I../bst
LDFLAGS += -I../vcas_bst
LDFLAGS += -I../bslack_reuse
LDFLAGS += -I../citrus
LDFLAGS += -I../common
LDFLAGS += -I../dcss_plus
LDFLAGS += -I../descriptors
LDFLAGS += -I../include
LDFLAGS += -I../lazylist
LDFLAGS += -I../lockfree_list
LDFLAGS += -I../lockfree_skiplist
LDFLAGS += -I../skiplist_lock
LDFLAGS += -I../microbench
LDFLAGS += -I../recordmgr
LDFLAGS += -I../rlu
LDFLAGS += -I../rlu_citrus
LDFLAGS += -I../rlu_linked_list
LDFLAGS += -I../rq
LDFLAGS += -I../rq/snapcollector

# Bundle specific includes.
LDFLAGS += -I../bundle
LDFLAGS += -I../bundle_lazylist
LDFLAGS += -I../bundle_skiplist_lock
LDFLAGS += -I../bundle_citrus
LDFLAGS += -I../bundle_bst
# -------------------------

# vCAS specific includes
LDFLAGS += -I../vcas_bst
LDFLAGS += -I../vcas_lazylist
LDFLAGS += -I../vcas_skiplist_lock
LDFLAGS += -I../vcas_citrus
LDFLAGS += -I../vcas_lockfree_skiplist
LDFLAGS += -I../vcas_lockfree_list
# -------------------------

# mvccvbr specific includes
LDFLAGS += -I../mvccvbr
LDFLAGS += -I../unsafe_vbr
# -------------------------

# Unsafe specific includes.
LDFLAGS += -I../unsafe/lazylist/
LDFLAGS += -I../unsafe/skiplist_lock/
LDFLAGS += -I../unsafe/citrus/
# -------------------------

LDFLAGS += -lpthread
LDFLAGS += -ldl
LDFLAGS += -lnuma
LDFLAGS += -lpapi

machine=$(shell hostname)

#all: abtree bslack bst lazylist lflist citrus rlu skiplistlock lbundle ubundle
all: BRF EEMARQ CTS EBRQ UNSAFE



#.PHONY: lbundle
#lbundle: citrus.rq_lbundle skiplistlock.rq_lbundle lazylist.rq_lbundle bst.rq_lbundle

thispath=



.PHONY: lazylist lazylist.rq_lockfree lazylist.rq_rwlock lazylist.rq_htm_rwlock lazylist.rq_unsafe lazylist.rq_lbundle
lazylist: lazylist.rq_lockfree lazylist.rq_rwlock lazylist.rq_htm_rwlock lazylist.rq_unsafe lazylist.rq_lbundle
#lazylist.rq_lockfree:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLAZYLIST -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
#lazylist.rq_rwlock:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLAZYLIST -DRQ_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
# lazylist.rq_htm_rwlock:
# 	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLAZYLIST -DRQ_HTM_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
# lazylist.rq_unsafe:
# 	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLAZYLIST -DRQ_UNSAFE $(pinning) $(thispath)main.cpp $(LDFLAGS)
lazylist.rq_lbundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_LINKED_BUNDLE -DBUNDLE_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)


.PHONY: skiplistlock skiplistlock.rq_lockfree skiplistlock.rq_rwlock skiplistlock.rq_htm_rwlock skiplistlock.rq_unsafe skiplistlock.rq_snapcollector skiplistlock.rq_lbundle
skiplistlock: skiplistlock.rq_lockfree skiplistlock.rq_rwlock skiplistlock.rq_htm_rwlock skiplistlock.rq_unsafe skiplistlock.rq_snapcollector skiplistlock.rq_lbundle
skiplistlock.rq_lockfree:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DSKIPLISTLOCK -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplistlock.rq_rwlock:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DSKIPLISTLOCK -DRQ_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
# skiplistlock.rq_htm_rwlock:
# 	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DSKIPLISTLOCK -DRQ_HTM_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
# skiplistlock.rq_unsafe:
# 	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DSKIPLISTLOCK -DRQ_UNSAFE $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplistlock.rq_snapcollector:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DSKIPLISTLOCK -DRQ_SNAPCOLLECTOR $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplistlock.rq_lbundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_LINKED_BUNDLE -DBUNDLE_SKIPLIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
 
.PHONY: lockfreeskiplist lockfreeskiplist.rq_unsafe
lockfreeskiplist: lockfreeskiplist.rq_unsafe
lockfreeskiplist.rq_unsafe:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLFSKIPLIST -DRQ_UNSAFE $(pinning) $(thispath)main.cpp $(LDFLAGS)

.PHONY: bst bst.rq_lockfree bst.rq_rwlock bst.rq_htm_rwlock bst.rq_unsafe bst.rq_vcas bst.rq_lbundle
bst: bst.rq_lockfree bst.rq_rwlock bst.rq_htm_rwlock bst.rq_unsafe bst.rq_vcas bst.rq_lbundle
bst.rq_lockfree:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DBST -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
#bst.rq_rwlock:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(;ilesuffix).out $(xargs) -DBST -DRQ_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
# bst.rq_htm_rwlock:
# 	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DBST -DRQ_HTM_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
bst.rq_unsafe:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DBST -DRQ_UNSAFE $(pinning) $(thispath)main.cpp $(LDFLAGS)
bst.rq_vcas:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DVCASBST -DRQ_VCAS $(pinning) $(thispath)main.cpp $(LDFLAGS)
bst.rq_lbundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_LINKED_BUNDLE -DBUNDLE_BST $(pinning) $(thispath)main.cpp $(LDFLAGS)

.PHONY: citrus citrus.rq_lockfree citrus.rq_rwlock citrus.rq_htm_rwlock citrus.rq_unsafe citrus.rq_lbundle
citrus: citrus.rq_lockfree citrus.rq_rwlock citrus.rq_htm_rwlock citrus.rq_unsafe citrus.rq_lbundle citrus.rq_vcas
citrus.rq_lockfree:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DCITRUS -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
#citrus.rq_rwlock:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DCITRUS -DRQ_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
# citrus.rq_htm_rwlock:
# 	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DCITRUS -DRQ_HTM_RWLOCK $(pinning) $(thispath)main.cpp $(LDFLAGS)
# citrus.rq_unsafe:
# 	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DCITRUS -DRQ_UNSAFE $(pinning) $(thispath)main.cpp $(LDFLAGS)
#citrus.rq_lbundle:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_LINKED_BUNDLE -DBUNDLE_CITRUS $(pinning) $(thispath)main.cpp $(LDFLAGS)
#citrus.rq_vcas:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DVCAS_CITRUS -DRQ_VCAS $(pinning) $(thispath)main.cpp $(LDFLAGS)

.PHONY: RLU list.rq_RLU tree.rq_RLU
RLU: list.rq_RLU tree.rq_RLU
list.rq_RLU:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRLU_LIST $(pinning) $(thispath)main.cpp $(thispath)../rlu/rlu.cpp $(LDFLAGS)
tree.rq_RLU:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRLU_CITRUS $(pinning) $(thispath)main.cpp $(thispath)../rlu/rlu.cpp $(LDFLAGS)

.PHONY: ubundle lazylist.rq_ubundle skiplistlock.rq_ubundle citrus.rq_ubundle 
ubundle: lazylist.rq_ubundle skiplistlock.rq_ubundle citrus.rq_ubundle 
lazylist.rq_ubundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_UNSAFE_BUNDLE -DBUNDLE_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplistlock.rq_ubundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_UNSAFE_BUNDLE -DBUNDLE_SKIPLIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
citrus.rq_ubundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_UNSAFE_BUNDLE -DBUNDLE_CITRUS $(pinning) $(thispath)main.cpp $(LDFLAGS)

## The following is an experimental bundle implementation that uses a circular buffer instead of a linked list.
.PHONY: cbundle lazylist.rq_cbundle skiplistlock.rq_cbundle citrus.rq_cbundle
cbundle: lazylist.rq_cbundle skiplistlock.rq_cbundle citrus.rq_cbundle
lazylist.rq_cbundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_CIRCULAR_BUNDLE -DBUNDLE_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplistlock.rq_cbundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_CIRCULAR_BUNDLE -DBUNDLE_SKIPLIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
citrus.rq_cbundle:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_CIRCULAR_BUNDLE -DBUNDLE_CITRUS $(pinning) $(thispath)main.cpp $(LDFLAGS)

#.PHONY: unsafe lazylist.rq_unsafe skiplistlock.rq_unsafe citrus.rq_unsafe
#unsafe: lazylist.rq_unsafe skiplistlock.rq_unsafe citrus.rq_unsafe
#lazylist.rq_unsafe:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DUNSAFE_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
#skiplistlock.rq_unsafe:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DUNSAFE_SKIPLIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
#citrus.rq_unsafe:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DUNSAFE_CITRUS $(pinning) $(thispath)main.cpp $(LDFLAGS)

#.PHONY: lflist lflist.rq_unsafe lflist.rq_lockfree
#lflist: lflist.rq_unsafe lflist.rq_lockfree
#lflist.rq_unsafe:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLFLIST -DRQ_UNSAFE $(pinning) $(thispath)main.cpp $(LDFLAGS)
#lflist.rq_lockfree:
#	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLFLIST -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)

.PHONY: BRF skiplist.rq_BRF tree.rq_BRF list.rq_BRF
BRF: skiplist.rq_BRF tree.rq_BRF list.rq_BRF
list.rq_BRF:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_LINKED_BUNDLE -DBUNDLE_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplist.rq_BRF:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_LINKED_BUNDLE -DBUNDLE_SKIPLIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
tree.rq_BRF:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DRQ_BUNDLE -DBUNDLE_LINKED_BUNDLE -DBUNDLE_CITRUS $(pinning) $(thispath)main.cpp $(LDFLAGS)

.PHONY: EBRQ skiplist.rq_EBRQ tree.rq_EBRQ list.rq_EBRQ
EBRQ: skiplist.rq_EBRQ tree.rq_EBRQ list.rq_EBRQ
list.rq_EBRQ:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DLFLIST -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplist.rq_EBRQ:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DSKIPLISTLOCK -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
tree.rq_EBRQ:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DBST -DRQ_LOCKFREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
 
.PHONY: UNSAFE skiplist.rq_Unsafe tree.rq_Unsafe list.rq_Unsafe
UNSAFE: skiplist.rq_Unsafe tree.rq_Unsafe list.rq_Unsafe
list.rq_Unsafe:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DUNSAFE_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplist.rq_Unsafe:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DUNSAFE_SKIPLIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
tree.rq_Unsafe:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DUNSAFE_CITRUS $(pinning) $(thispath)main.cpp $(LDFLAGS)
 
.PHONY: vbrunsafe skiplist.rq_vbrunsafe tree.rq_vbrunsafe list.rq_vbrunsafe
vbrunsafe: skiplist.rq_vbrunsafe tree.rq_vbrunsafe list.rq_vbrunsafe
list.rq_vbrunsafe:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DVBR_UNSAFE_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)


.PHONY: EEMARQ skiplist.rq_EEMARQ tree.rq_EEMARQ list.rq_EEMARQ
EEMARQ: skiplist.rq_EEMARQ tree.rq_EEMARQ list.rq_EEMARQ
skiplist.rq_EEMARQ:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DMVCC_VBR_SKIPLIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
tree.rq_EEMARQ:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DMVCC_VBR_TREE $(pinning) $(thispath)main.cpp $(LDFLAGS)
list.rq_EEMARQ:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DMVCC_VBR_LIST $(pinning) $(thispath)main.cpp $(LDFLAGS)
 
.PHONY: CTS tree.rq_CTS skiplist.rq_CTS list.rq_CTS
CTS: tree.rq_CTS skiplist.rq_CTS list.rq_CTS
tree.rq_CTS:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DVCASBST -DRQ_VCAS $(pinning) $(thispath)main.cpp $(LDFLAGS)
skiplist.rq_CTS:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DVCAS_LOCKFREE_SKIPLIST -DRQ_VCAS $(pinning) $(thispath)main.cpp $(LDFLAGS)
list.rq_CTS:
	$(GPP) $(FLAGS) -o $(thispath)$(machine).$@$(filesuffix).out $(xargs) -DVCAS_LOCKFREE_LIST -DRQ_VCAS $(pinning) $(thispath)main.cpp $(LDFLAGS)

.PHONY: clean
clean:
	rm *.out
