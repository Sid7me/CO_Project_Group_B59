instruction={'add':'10000','sub':'10001','mov':'10010','ld':'10100','st':'10101',
             'mul':'10110','div':'10111','rs':'11000','ls':'11001','xor':'11010',
             'or':'11011','and':'11100','not':'11101','cmp':'11110','jmp':'11111',
             'jlt':'01100','jgt':'01101','je':'01111','hlt':'01010'}
registers={'R0':{'add':'000','value':0},'R1':{'add':'001','value':0},'R2':{'add':'010','value':0},'R3':{'add':'011','value':0},'R4':{'add':'100','value':0},'R5':{'add':'101','value':0},'R6':{'add':'110','value':0},'FLAGS':{'add':'111','value':0}}
var,program,linenumber,label,counter={},[],0,{},0
var1,label1=[],[]
flagchange,w=0,0
import sys
S= sys.stdin.read()
lines= S.split("\n")
for i in lines:
    line=i.split()
    program.append(line)
for i in range(len(program)):
    if program[i][0]=="var":
        if len(program[i])==1:
            print("No variable Name given Line Number",i+1)
            w=3
            break
        var[program[i][1]]=0
        var1.append(program[i][1])
    if ":" in program[i][0]:
        if len(program[i])==1:
            print("Label Not followed by instruction Line Number",i+1)
            w=3
            break
        label[program[i][0][0:len(program[i][0])-1]]=i+1
        a = program[i][0][0:len(program[i][0]) - 1]
        program[i].remove(program[i][0])
        label1.append(a)
while(linenumber<len(program)):
    if w==3:
        break
    if program[len(program)-1][0]!="hlt":
        print("Invalid Use of halt", linenumber + 1)
        break
    counter=0
    l1=program[linenumber]
    if l1[0]!="var" and l1[0] not in instruction:
        print("Invalid Instruction Line Number",linenumber+1)
        break
    p=""
    if flagchange==0:
        registers['FLAGS']['value']=0
    flagchange=0
    if l1[0]!="var":
        if (len (l1)==3):
            if l1[0]=="mov":
                x=list(l1[2])
                if l1[1] not in registers or l1[2]=="FLAGS" or l1[1]=="FLAGS":
                    print("Invalid register Line Number",linenumber+1)
                    break
                if x[0]=="$":
                    x.remove('$')
                    t=""
                    for i in range(len(x)):
                        t=t+str(x[i])
                    t=t.isdigit()
                    if t==False:
                        print("Invalid Immediate Value Line Number",linenumber+1)
                        break
                    a=""
                    for i in range(len(x)):
                        a=a+str(int(x[i]))
                    a=int(a)
                    if a>256:
                        print("Out of Bound Value Line Number", linenumber + 1)
                        break
                    registers[l1[1]]['value']=a
                    p=p+str(instruction.get(l1[0]))+registers[l1[1]]['add']+str(format(registers[l1[1]]['value'],'08b'))
                else:
                    registers[l1[2]]['value']=registers[l1[1]]['value']
                    p=p+"100110000"+registers[l1[1]]['add']+registers[l1[2]]['add']
            elif l1[0] == "div":
                registers['R1']['value']=registers[l1[1]]%registers[l1[2]]['value']
                registers['R0']['value']=registers[l1[1]]//registers[l1[2]]['value']
                p=p+"101110000"+registers[l1[1]]['add']+registers[l1[2]]['add']
            elif l1[0]=="not":
                if l1[1] not in registers or l1[2] not in registers or l1[1] == "FLAGS" or l1[3] == "FLAGS" :
                    print("Invalid register Line Number", linenumber + 1)
                    break
                registers[l1[2]]['value']=~registers[l1[1]]['value']
                p=p+instruction[l1[0]]+"00000"+registers[l1[1]]['add']+registers[l1[2]]['add']
            elif  l1[0]=="ld":
                if l1[1] not in registers or l1[2]=="FLAGS":
                    print("Invalid register Line Number",linenumber+1)
                    break
                if l1[2] not in var:
                    print("Invalid Variable Line Number", linenumber + 1)
                    break
                registers[l1[1]]['value']=var[l1[2]]
                num=len(program)-(var1.index(l1[2])+1)
                p=p+instruction[l1[0]]+registers[l1[1]]['add']+str(format(num, '08b'))
            elif l1[0]=="st":
                if l1[1] not in registers or l1[2]=="FLAGS":
                    print("Invalid register Line Number",linenumber+1)
                    break
                if l1[2] not in var:
                    print("Invalid Variable Line Number", linenumber + 1)
                var[l1[2]]=registers[l1[1]]['value']
                num=len(program) - (var1.index(l1[2]) + 1)
                p=p+instruction[l1[0]] + registers[l1[1]]['add'] + str(format(num, '08b'))
            elif l1[0] == "rs" or l1[0]=="ls":
                x=list(l1[2])
                x.remove('$')
                t = ""
                for i in range(len(x)):
                    t = t + str(x[i])
                t = t.isdigit()
                if t == False:
                    print("Invalid Immediate Value Line Number", linenumber + 1)
                    break
                a=""
                for i in range(len(x)):
                    a = a + str(int(x[i]))
                a = int(a)
                if l1[0] == "rs":
                    var[l1[2]]['value']//=(2**a)
                else:
                    var[l1[2]]['value']*=(2**a)
                p=p+instruction[l1[0]]+registers[l1[1]]['add'] + str(format(a, '08b'))
            elif l1[0]=="cmp":
                if l1[1] not in registers or l1[2] not in registers or l1[1] == "FLAGS" or l1[3] == "FLAGS" :
                    print("Invalid register Line Number", linenumber + 1)
                    break
                if registers[l1[1]]['value']>registers[l1[2]]['value']:
                    registers['FLAGS']['value']=2
                elif registers[l1[1]]['value']<registers[l1[2]]['value']:
                    registers['FLAGS']['value']=4
                else:
                    registers['FLAGS']['value']=1

        elif (len (l1)==4):
            if l1[1] not in registers or l1[2] not in registers or l1[3] not in registers or l1[1]== "FLAGS" or l1[3]== "FLAGS" or l1[2] == "FLAGS" :
                print("Invalid register Line Number", linenumber + 1)
                break
            if l1[0]=="add":
                registers[l1[3]]['value']=registers[l1[1]]['value']+registers[l1[2]]['value']
                registers['FLAGS']['value']=8
                flagchange = 1
            elif l1[0]=="sub":
                if registers[l1[1]]['value']<registers[l1[2]]['value']:
                    registers[l1[3]]['value']=0
                    registers['FLAGS']['value'] = 8
                    flagchange = 1
                else:
                 registers[l1[3]]['value']=registers[l1[1]]['value']-registers[l1[2]]['value']
            elif l1[0] == "mul":
                registers[l1[3]]['value']=registers[l1[1]]['value']*registers[l1[2]]['value']
                if registers[l1[3]]['value']>65535:
                    registers[l1[3]]['value']=0
                    registers['FLAGS']['value']=8
                    flagchange=1
            elif l1[0] == "xor":
                registers[l1[3]]['value'] = registers[l1[1]]['value']^registers[l1[2]]['value']
            elif l1[0] == "or":
                registers[l1[3]]['value'] = registers[l1[1]]['value']|registers[l1[2]]['value']
            elif l1[0] == "and":
                registers[l1[3]]['value'] = registers[l1[1]]['value']&registers[l1[2]]['value']
            p=p+instruction[l1[0]]+"00"+registers[l1[1]]['add']+registers[l1[2]]['add']+registers[l1[3]]['add']
        elif (len(l1) == 2) and l1[0]!="var":
            if l1[1] not in label:
                print("Invalid Label Line Number",linenumber+1)
                break
            if l1[0] == "jmp":
                linenumber=label[l1[1]]-1
                counter=1
            elif l1[0] == "jlt":
                if registers['FLAGS']['value']==4:
                    linenumber=label[l1[1]]-1
                    counter=1
                    flagchange = 1
            elif l1[0] == "jgt":
                if registers['FLAGS']['value']==2:
                    linenumber=label[l1[1]]-1
                    counter=1
                    flagchange = 1
            elif l1[0] == "je":
                if registers['FLAGS']['value']==1:
                    linenumber=label[l1[1]]-1
                    counter=1
                    flagchange = 1
            num=len(program)-(label1.index(l1[1])+1)-len(var1)
            p=p+instruction[l1[0]]+"000"+str(format(num,'08b'))
        elif l1[0]=="hlt":
            p=p+instruction[l1[0]]+"00000000000"
            sys.stdout.write(p)
            sys.stdout.write('\n')
            break
    if counter==0:
        linenumber+=1
    sys.stdout.write(p)
    sys.stdout.write('\n')