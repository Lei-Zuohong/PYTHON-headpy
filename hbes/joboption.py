# -*- coding: UTF-8 -*-
'''
This is a package document.

    Environment version:

        etc

    Content:

        @etc:
            etc
'''
# Public package
import os
import re
import sys
import random
# Private package
import headpy.hscreen.hprint as hprint


def addfolder(name, path):
    '查看某绝对路径下是否存在某名字的文件夹，没有则创建'
    filelist = os.listdir(path)
    if(name not in filelist):
        os.system('mkdir %s/%s' % (path, name))


def sim(txtfile='',
        decfile='',
        datfile='',
        parent='',
        runid=[0, 0],
        rtrawfile='',
        datalevel=0,
        events=0,
        condor=0):
    '生成MC joboption文件并运行'
    seed = random.randint(0, 99)
    line = []
    line.append(
        '#include "$OFFLINEEVENTLOOPMGRROOT/share/OfflineEventLoopMgr_Option.txt"')
    line.append('#include "$BESEVTGENROOT/share/BesEvtGen.txt"')
    line.append('#include "$BESSIMROOT/share/Bes_Gen.txt"')
    line.append('#include "$BESSIMROOT/share/G4Svc_BesSim.txt"')
    line.append('#include "$CALIBSVCROOT/share/calibConfig_sim.txt"')
    line.append('#include "$ROOTIOROOT/share/jobOptions_Digi2Root.txt"')
    # 添加随机数因子
    line.append('BesRndmGenSvc.RndmSeed = %d;' % (seed))
    # 添加decay card
    if(decfile != ''):
        line.append('EvtDecay.userDecayTableName = "%s";' % (decfile))
    # 添加dat文件
    if(datfile != ''):
        line.append('EvtDecay.FileForTrackGen = {"%s"};' % (datfile))
    # 添加母粒子
    if(parent != ''):
        line.append('EvtDecay.ParentParticle = "%s";' % (parent))
    # 添加run号
    if(runid != [0, 0]):
        line.append(
            'RealizationSvc.RunIdList = {-%d, 0, -%d};' % (runid[1], runid[0]))
    # 添加输出文件
    if(rtrawfile != ''):
        line.append('RootCnvSvc.digiRootOutputFile = "%s";' % (rtrawfile))
    # 添加输出数据等级
    if(datalevel != 0):
        line.append('MessageSvc.OutputLevel  = %d;' % (datalevel))
    # 添加输出数据量
    if(datalevel != 0):
        line.append('ApplicationMgr.EvtMax = %d;' % (events))
    # 特殊分波方法，选择性注释掉
    line.append('EvtDecay.statDecays = true;')
    line.append('EvtDecay.DecayTopology="EvtTop";')
    line.append('ApplicationMgr.DLLs += { "BesServices"};')
    # 整合line并输出
    output = ''
    for i in line:
        output += i+'\n'
    with open(txtfile, 'w') as outfile:
        outfile.write(output)
    if(condor == '1'):
        os.system('boss.condor %s' % (txtfile))


def dosim(txtfolder='',
          decfolder='',
          datfolder='',
          rtrawfolder='',
          datalevel=6,
          energy_list=0,
          parent='vpho',
          files=0,
          events=0,
          energy=0,
          condor=0):
    # 输出数据
    hprint.pstar()
    hprint.ppoint('txt folder', txtfolder)
    hprint.ppoint('dec folder', decfolder)
    hprint.ppoint('dat folder', datfolder)
    hprint.ppoint('rtraw folder', rtrawfolder)
    hprint.ppoint('number of files', files)
    hprint.ppoint('number of events', events)
    if(condor == '1'):
        hprint.ppoint('submit job', 'yes')
    else:
        hprint.ppoint('submit job', 'no')
    # 运行单个能量点
    if(float(energy) in energy_list):
        energy = float(energy)
        hprint.ppoint('energy', '%1.4f' % (energy))
        hprint.pstar()
        for i1 in range(files):
            # 填充txtfile
            txtfile = '%s/%1.4f_%02d.txt' % (txtfolder, energy, i1)
            # 填充decfile
            if(decfolder != ''):
                decfile = '%s/%1.4f.dec' % (decfolder, energy)
            else:
                decfile = ''
            # 填充datfile
            if(datfolder != ''):
                datfile = '%s/%05d.dat' % (datfolder, 10000*energy)
            else:
                datfile = ''
            # 填充runid
            runid = [energy_list[energy][0], energy_list[energy][1]]
            # 填充rtrawfile
            if(rtrawfolder != ''):
                rtrawfile = '%s/%1.4f_%02d.rtraw' % (rtrawfolder, energy, i1)
            else:
                rtrawfile = ''
            sim(txtfile,
                decfile=decfile,
                datfile=datfile,
                parent=parent,
                runid=runid,
                rtrawfile=rtrawfile,
                datalevel=datalevel,
                events=events,
                condor=condor)
    # 运行所有能量点
    elif(float(energy) == -1):
        hprint.ppoint('energy', 'all')
        hprint.pstar()
        for energy in energy_list:
            for i1 in range(files):
                # 填充txtfile
                txtfile = '%s/%1.4f_%02d.txt' % (txtfolder, energy, i1)
                # 填充decfile
                if(decfolder != ''):
                    decfile = '%s/%1.4f.dec' % (decfolder, energy)
                else:
                    decfile = ''
                # 填充datfile
                if(datfolder != ''):
                    datfile = '%s/%05d.dat' % (datfolder, 10000*energy)
                else:
                    datfile = ''
                # 填充runid
                runid = [energy_list[energy][0], energy_list[energy][1]]
                # 填充rtrawfile
                if(rtrawfolder != ''):
                    rtrawfile = '%s/%1.4f_%02d.rtraw' % (
                        rtrawfolder, energy, i1)
                else:
                    rtrawfile = ''
                sim(txtfile,
                    decfile=decfile,
                    datfile=datfile,
                    parent=parent,
                    runid=runid,
                    rtrawfile=rtrawfile,
                    datalevel=datalevel,
                    events=events,
                    condor=condor)
    else:
        print('能量点选项输入错误')


def rec(txtfile,
        rtrawfile,
        dstfile,
        condor):
    'Reconstruct a rtraw file'
    seed = random.randint(0, 99)
    line = []
    line.append('#include "$ROOTIOROOT/share/jobOptions_ReadRoot.txt"')
    line.append('#include "$ROOTIOROOT/share/jobOptions_ReadRoot.txt"')
    line.append(
        '#include "$OFFLINEEVENTLOOPMGRROOT/share/OfflineEventLoopMgr_Option.txt"')
    line.append(
        '#include "$BESEVENTMIXERROOT/share/jobOptions_EventMixer_rec.txt"')
    line.append('#include "$CALIBSVCROOT/share/job-CalibData.txt"')
    line.append('#include "$MAGNETICFIELDROOT/share/MagneticField.txt"')
    line.append('#include "$ESTIMEALGROOT/share/job_EsTimeAlg.txt"')
    line.append('#include "$MDCXRECOROOT/share/jobOptions_MdcPatTsfRec.txt"')
    line.append('#include "$KALFITALGROOT/share/job_kalfit_numf_data.txt"')
    line.append('#include "$MDCDEDXALGROOT/share/job_dedx_all.txt"')
    line.append('#include "$TRKEXTALGROOT/share/TrkExtAlgOption.txt"')
    line.append('#include "$TOFRECROOT/share/jobOptions_TofRec.txt"')
    line.append('#include "$TOFENERGYRECROOT/share/TofEnergyRecOptions_MC.txt"')
    line.append('#include "$EMCRECROOT/share/EmcRecOptions.txt"')
    line.append('#include "$MUCRECALGROOT/share/jobOptions_MucRec.txt"')
    line.append('#include "$EVENTASSEMBLYROOT/share/EventAssembly.txt"')
    line.append('#include "$PRIMARYVERTEXALGROOT/share/jobOptions_kalman.txt"')
    line.append('#include "$VEEVERTEXALGROOT/share/jobOptions_veeVertex.txt"')
    line.append('#include "$HLTMAKERALGROOT/share/jobOptions_HltMakerAlg.txt"')
    line.append('#include "$EVENTNAVIGATORROOT/share/EventNavigator.txt"')
    line.append('#include "$ROOTIOROOT/share/jobOptions_Dst2Root.txt"')
    line.append('#include "$CALIBSVCROOT/share/calibConfig_rec_mc.txt"')
    line.append('BesRndmGenSvc.RndmSeed = %d;' % (seed+100))
    line.append('MessageSvc.OutputLevel = 6;')
    line.append('EventCnvSvc.digiRootInputFile = {"%s"};' % (rtrawfile))
    line.append('EventCnvSvc.digiRootOutputFile ="%s";' % (dstfile))
    line.append('ApplicationMgr.EvtMax = -1;')
    output = ''
    for i in line:
        output += i+'\n'
    with open(txtfile, 'w') as outfile:
        outfile.write(output)
    if(condor == '1'):
        os.system('boss.condor %s' % (txtfile))


def dorec(txtfolder,
          rtrawfolder,
          dstfolder,
          condor='0'):
    'Reconstruct all rtraw files'
    hprint.pstar()
    hprint.ppoint('Location of .txt', txtfolder)
    hprint.ppoint('Location of .rtraw', rtrawfolder)
    hprint.ppoint('Location of .dst', dstfolder)
    hprint.pstar()
    if(condor == '1'):
        hprint.ppoint('Submit job', 'Yes')
        hprint.pstar()
    else:
        hprint.ppoint('Submit job', 'No')
        hprint.pstar()
    rtrawlist = os.listdir(rtrawfolder)
    num = len(rtrawlist)
    hprint.ppoint('Number of jobs', num)
    hprint.pstar()
    for i in rtrawlist:
        method = r'(.*).rtraw'
        match = re.match(method, i)
        filename = match.group(1)
        rec('%s/%s.txt' % (txtfolder, filename),
            '%s/%s' % (rtrawfolder, i),
            '%s/%s.dst' % (dstfolder, filename),
            condor)


def alg(algroot,
        txtfile,
        dst_list,
        rootfile,
        option_list,
        condor):
    'Analysis a dst file'
    line = []
    # deal with head file
    line.append('#include "$ROOTIOROOT/share/jobOptions_ReadRec.txt"')
    line.append('#include "$VERTEXFITROOT/share/jobOptions_VertexDbSvc.txt"')
    line.append('#include "$MAGNETICFIELDROOT/share/MagneticField.txt"')
    line.append('#include "$ABSCORROOT/share/jobOptions_AbsCor.txt"')
    line.append('#include "$%s/share/%s"' % (algroot[0], algroot[1]))
    # deal with option_list
    for i in option_list:
        line.append('%s;' % (i))
    # deal with dst_list
    dstfile = ''
    for i in dst_list:
        dstfile = dstfile + '"%s"' % (i) + ',' + '\n'
    dstfile = dstfile[:-2]
    line.append('EventCnvSvc.digiRootInputFile = {%s};' % (dstfile))
    # deal with other
    line.append('MessageSvc.OutputLevel = 6;')
    line.append('ApplicationMgr.EvtMax = -1;')
    line.append('ApplicationMgr.HistogramPersistency = "ROOT";')
    line.append(
        'NTupleSvc.Output = { "FILE1 DATAFILE=\'%s\' OPT=\'NEW\' TYP=\'ROOT\'"};' % (rootfile))
    output = ''
    for i in line:
        output += i+'\n'
    with open(txtfile, 'w') as outfile:
        outfile.write(output)
    if(condor == '1'):
        os.system('boss.condor %s' % (txtfile))


def doalg(algroot,
          txtfolder,
          dstfolder,
          rootfolder,
          options,
          condor='0'):
    'Analysis all dst files'
    hprint.pstar()
    hprint.ppoint('Location of .txt', txtfolder)
    hprint.ppoint('Location of .dst', dstfolder)
    hprint.ppoint('Location of .root', rootfolder)
    hprint.pstar()
    if(condor == '1'):
        hprint.ppoint('Submit job', 'Yes')
        hprint.pstar()
    else:
        hprint.ppoint('Submit job', 'No')
        hprint.pstar()
    dstlist = os.listdir(dstfolder)
    num = len(dstlist)
    hprint.ppoint('Number of jobs', num)
    hprint.pstar()
    # run
    for i in dstlist:
        method = r'(.*)_(.*).dst'
        match = re.match(method, i)
        filename = match.group(1) + '_' + match.group(2)
        option_list = options + ['%s.Energy = %s' %
                                 (algroot[2], match.group(1))]
        alg(algroot,
            '%s/%s.txt' % (txtfolder, filename),
            ['%s/%s' % (dstfolder, i)],
            '%s/%s.root' % (rootfolder, filename),
            option_list,
            condor)


class WORKSPACE:
    '整合工作参数，并执行操作'

    def __init__(self, version, name):
        self.version = version
        self.name = name
        self.path = {}
        # 初始化根目录地址
        self.path['scratchfs'] = '/scratchfs/bes/leizh'
        self.path['work'] = '%s/%s' % (self.path['scratchfs'], self.name)
        self.path['data'] = '%s/%s_data' % (self.path['scratchfs'], self.name)
        # 初始化工作区地址
        self.path['reala'] = '%s/reala' % (self.path['work'])
        self.path['backa'] = '%s/backa' % (self.path['work'])
        self.path['sima'] = '%s/sima' % (self.path['work'])
        self.path['dec'] = '%s/mc/dec' % (self.path['work'])
        self.path['sim'] = '%s/mc/sim' % (self.path['work'])
        self.path['rec'] = '%s/mc/rec' % (self.path['work'])
        # 初始化数据区地址
        self.path['realr'] = '%s/realr' % (self.path['data'])
        self.path['backr'] = '%s/backr' % (self.path['data'])
        self.path['simr'] = '%s/simr' % (self.path['data'])
        self.path['rtraw'] = '%s/rtraw' % (self.path['data'])
        self.path['dst'] = '%s/dst' % (self.path['data'])
        # 读取能量点和分析包数据
        self.energy_list = {}
        self.algroot = []
        exec('import headpy.hbes.h%s as ana' % (name))
        exec('self.energy_list = ana.energy_list()')
        exec('self.algroot = ana.algroot()')

    def dodec(self, method, content=''):
        '用来在相应位置产生dec文件'
        if(content == ''):
            print('请输入dec文件内容')
        else:
            addfolder(method, self.path['dec'])
            filedec = '%s/%s' % (self.path['dec'], method)
            for i in self.energy_list:
                with open('%s/%1.4f.dec' % (filedec, i), 'w') as outfile:
                    output = content.replace('replace_energy', '%1.4f' % (i))
                    outfile.write(output)
                print('已创建能量点%1.4f.dec文件' % (i))

    def dosim(self, method,
              dopw='',
              files=10,
              events=10000,
              condor='0',
              energy='-1'):
        '用来生成sim文件并运行'
        addfolder(method, self.path['sim'])
        addfolder(method, self.path['rtraw'])
        self.energy_list[2.0000][1] = 41814
        if(dopw == ''):
            dosim(txtfolder='%s/%s' % (self.path['sim'], method),
                  decfolder='%s/%s' % (self.path['dec'], method),
                  rtrawfolder='%s/%s' % (self.path['rtraw'], method),
                  energy_list=self.energy_list,
                  files=files,
                  events=events,
                  condor=condor,
                  energy=energy)
        else:
            dosim(txtfolder='%s/%s' % (self.path['sim'], method),
                  decfolder='%s/%s' % (self.path['dec'], method),
                  datfolder='%s/%s' % (self.path['dec'], method),
                  rtrawfolder='%s/%s' % (self.path['rtraw'], method),
                  energy_list=self.energy_list,
                  files=files,
                  events=events,
                  condor=condor,
                  energy=energy)

    def dorec(self, method,
              condor='0'):
        '用来生成rec文件并运行'
        addfolder(method, self.path['rec'])
        addfolder(method, self.path['dst'])
        dorec('%s/%s' % (self.path['rec'], method),
              '%s/%s' % (self.path['rtraw'], method),
              '%s/%s' % (self.path['dst'], method),
              condor=condor)

    def dosima(self, method,
               option_list=[],
               condor='0'):
        '用来生成ana文件并运行'
        addfolder(method, self.path['sima'])
        addfolder(method, self.path['simr'])
        doalg(self.algroot,
              '%s/%s' % (self.path['sima'], method),
              '%s/%s' % (self.path['dst'], method),
              '%s/%s' % (self.path['simr'], method),
              option_list,
              condor)
