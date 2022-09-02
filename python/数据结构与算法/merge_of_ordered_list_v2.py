"""有序表的合并-链表实现"""
from single_linked_list import SingleLinkedList


lla = SingleLinkedList()
llb = SingleLinkedList()
llc = SingleLinkedList()
for i in [1, 7, 8]:
    lla.append(i)
for j in [2, 4, 6, 8, 10, 11]:
    llb.append(j)

pa, pb = lla.head.next_, llb.head.next_
pc = llc.head = lla.head
while pa and pb:
    if pa.elem <= pb.elem:
        pc.next_ = pa
        pc = pa
        pa = pa.next_
    else:
        pc.next_ = pb
        pc = pb
        pb = pb.next_

if pa:
    pc.next_ = pa
else:
    pc.next_ = pb

del llb.head
