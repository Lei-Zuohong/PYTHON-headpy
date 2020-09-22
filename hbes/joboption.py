# -*- coding: UTF-8 -*-
# Public package
import os
import re
import random
# Private package
import headpy.hscreen.hprint as hprint

# MC 产生重建类函数


def addfolder(name, path):
    '查看某绝对路径下是否存在某名字的文件夹，没有则创建'
    filelist = os.listdir(path)
    if(name not in filelist):
        os.system('mkdir %s/%s' % (path, name))


def sim(txt_file='',
        dec_file='',
        dat_file='',
        parent='vpho',
        usediy=0,
        runid=[0, 0],
        rtraw_file='',
        datalevel=0,
        events=0,
        option_list=[],
        condor='0'):
    '生成MC joboption文件并运行'
    seed = random.randint(0, 99)
    line = []
    line.append('//****************************************')
    line.append('#include "$OFFLINEEVENTLOOPMGRROOT/share/OfflineEventLoopMgr_Option.txt"')
    line.append('//****************************************')
    # 添加Other line
    for i in option_list:
        line.append(i)
    line.append('//****************************************')
    # 添加decay card
    line.append('#include "$BESEVTGENROOT/share/BesEvtGen.txt"')
    if(dec_file != ''):
        line.append('EvtDecay.userDecayTableName = "%s";' % (dec_file))
    line.append('//****************************************')
    # 添加随机数因子
    line.append('BesRndmGenSvc.RndmSeed = %d;' % (seed))
    line.append('//****************************************')
    # 添加其他类
    line.append('#include "$BESSIMROOT/share/G4Svc_BesSim.txt"')
    line.append('#include "$CALIBSVCROOT/share/calibConfig_sim.txt"')
    # 添加run号
    if(runid != [0, 0]):
        line.append(
            'RealizationSvc.RunIdList = {-%d, 0, -%d};' % (runid[1], runid[0]))
    line.append('//****************************************')
    # 添加输出文件
    line.append('#include "$ROOTIOROOT/share/jobOptions_Digi2Root.txt"')
    if(rtraw_file != ''):
        line.append('RootCnvSvc.digiRootOutputFile = "%s";' % (rtraw_file))
    line.append('//****************************************')
    # 添加输出数据等级
    if(datalevel != 0):
        line.append('MessageSvc.OutputLevel  = %d;' % (datalevel))
    # 添加输出数据量
    if(events != 0):
        line.append('ApplicationMgr.EvtMax = %d;' % (events))
    line.append('//****************************************')
    # 添加dat文件
    if(dat_file != ''):
        line.append('EvtDecay.FileForTrackGen = {"%s"};' % (dat_file))
    # 添加母粒子
    if(parent != ''):
        line.append('EvtDecay.ParentParticle = "%s";' % (parent))
    line.append('//****************************************')
    line.append('#include "$BESSIMROOT/share/Bes_Gen.txt"')
    # 特殊分波方法，选择性注释掉
    line.append('EvtDecay.statDecays = true;')
    line.append('EvtDecay.DecayTopology="EvtTop";')
    line.append('ApplicationMgr.DLLs += { "BesServices"};')
    line.append('//****************************************')
    # 添加DIY
    if(usediy != 0):
        line.append('EvtDecay.statDecays = true;')
        line.append('EvtDecay.mDIY = true;')
    line.append('//****************************************')
    # 整合line并输出
    output = ''
    for i in line:
        output += i + '\n'
    with open(txt_file, 'w') as outfile:
        outfile.write(output)
    if(condor == '1'):
        os.system('boss.condor %s' % (txt_file))


def dosim(txt_folder='',
          dec_folder='',
          dat_folder='',
          rtraw_folder='',
          parent='vpho',
          usediy=0,
          energy_list=0,
          energy=0,
          datalevel=6,
          files=0,
          events=0,
          option_list=[],
          condor='0'):
    # 输出数据
    hprint.pstar()
    hprint.ppoint('txt folder', txt_folder)
    hprint.ppoint('dec folder', dec_folder)
    hprint.ppoint('dat folder', dat_folder)
    hprint.ppoint('rtraw folder', rtraw_folder)
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
            # 填充txt_file
            txt_file = '%s/%1.4f_%02d.txt' % (txt_folder, energy, i1)
            # 填充dec_file
            if(dec_folder != ''):
                dec_file = '%s/%1.4f.dec' % (dec_folder, energy)
            else:
                dec_file = ''
            # 填充dat_file
            if(dat_folder != ''):
                dat_file = '%s/%05d.dat' % (dat_folder, 10000 * energy)
            else:
                dat_file = ''
            # 填充runid
            runid = [energy_list[energy][0], energy_list[energy][1]]
            # 填充rtraw_file
            if(rtraw_folder != ''):
                rtraw_file = '%s/%1.4f_%02d.rtraw' % (rtraw_folder, energy, i1)
            else:
                rtraw_file = ''
            sim(txt_file=txt_file,
                dec_file=dec_file,
                dat_file=dat_file,
                parent=parent,
                usediy=usediy,
                runid=runid,
                rtraw_file=rtraw_file,
                datalevel=datalevel,
                events=events,
                option_list=option_list,
                condor=condor)
    # 运行所有能量点
    elif(float(energy) == -1):
        hprint.ppoint('energy', 'all')
        hprint.pstar()
        for energy in energy_list:
            for i1 in range(files):
                # 填充txt_file
                txt_file = '%s/%1.4f_%02d.txt' % (txt_folder, energy, i1)
                # 填充dec_file
                if(dec_folder != ''):
                    dec_file = '%s/%1.4f.dec' % (dec_folder, energy)
                else:
                    dec_file = ''
                # 填充datfile
                if(dat_folder != ''):
                    dat_file = '%s/%05d.dat' % (dat_folder, 10000 * energy)
                else:
                    dat_file = ''
                # 填充runid
                runid = [energy_list[energy][0], energy_list[energy][1]]
                # 填充rtrawfile
                if(rtraw_folder != ''):
                    rtraw_file = '%s/%1.4f_%02d.rtraw' % (
                        rtraw_folder, energy, i1)
                else:
                    rtraw_file = ''
                sim(txt_file=txt_file,
                    dec_file=dec_file,
                    dat_file=dat_file,
                    parent=parent,
                    usediy=usediy,
                    runid=runid,
                    rtraw_file=rtraw_file,
                    datalevel=datalevel,
                    events=events,
                    option_list=option_list,
                    condor=condor)
    else:
        print('能量点选项输入错误')


def rec(txt_file='',
        rtraw_file='',
        dst_file='',
        condor='0'):
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
    line.append('BesRndmGenSvc.RndmSeed = %d;' % (seed + 100))
    line.append('MessageSvc.OutputLevel = 6;')
    line.append('EventCnvSvc.digiRootInputFile = {"%s"};' % (rtraw_file))
    line.append('EventCnvSvc.digiRootOutputFile ="%s";' % (dst_file))
    line.append('ApplicationMgr.EvtMax = -1;')
    output = ''
    for i in line:
        output += i + '\n'
    with open(txt_file, 'w') as outfile:
        outfile.write(output)
    if(condor == '1'):
        os.system('boss.condor %s' % (txt_file))


def dorec(txt_folder='',
          rtraw_folder='',
          dst_folder='',
          condor='0'):
    'Reconstruct all rtraw files'
    hprint.pstar()
    hprint.ppoint('Location of .txt', txt_folder)
    hprint.ppoint('Location of .rtraw', rtraw_folder)
    hprint.ppoint('Location of .dst', dst_folder)
    hprint.pstar()
    if(condor == '1'):
        hprint.ppoint('Submit job', 'Yes')
        hprint.pstar()
    else:
        hprint.ppoint('Submit job', 'No')
        hprint.pstar()
    rtrawlist = os.listdir(rtraw_folder)
    num = len(rtrawlist)
    hprint.ppoint('Number of jobs', num)
    hprint.pstar()
    for i in rtrawlist:
        method = r'(.*).rtraw'
        match = re.match(method, i)
        filename = match.group(1)
        rec(txt_file='%s/%s.txt' % (txt_folder, filename),
            rtraw_file='%s/%s' % (rtraw_folder, i),
            dst_file='%s/%s.dst' % (dst_folder, filename),
            condor=condor)


def alg(algroot=[],
        txt_file='',
        root_file='',
        dst_list=[],
        option_list=[],
        condor='0'):
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
        'NTupleSvc.Output = { "FILE1 DATAFILE=\'%s\' OPT=\'NEW\' TYP=\'ROOT\'"};' % (root_file))
    output = ''
    for i in line:
        output += i + '\n'
    with open(txt_file, 'w') as outfile:
        outfile.write(output)
    if(condor == '1'):
        os.system('boss.condor %s' % (txt_file))


def doalg(algroot=[],
          txt_folder='',
          dst_folder='',
          root_folder='',
          options=[],
          condor='0'):
    'Analysis all dst files'
    hprint.pstar()
    hprint.ppoint('Location of .txt', txt_folder)
    hprint.ppoint('Location of .dst', dst_folder)
    hprint.ppoint('Location of .root', root_folder)
    hprint.pstar()
    if(condor == '1'):
        hprint.ppoint('Submit job', 'Yes')
        hprint.pstar()
    else:
        hprint.ppoint('Submit job', 'No')
        hprint.pstar()
    dstlist = os.listdir(dst_folder)
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
        alg(algroot=algroot,
            txt_file='%s/%s.txt' % (txt_folder, filename),
            root_file='%s/%s.root' % (root_folder, filename),
            dst_list=['%s/%s' % (dst_folder, i)],
            option_list=option_list,
            condor=condor)


class WORKSPACE:
    '''
    整合数据信息，操作工作函数\n
    dodec 提供衰变卡输入\n
    dosim 提供sim过程\n
    dorec 提供rec过程\n
    dosima 提供ana过程\n
    '''

    def __init__(self,
                 path_work='',
                 path_data='',
                 method='',
                 algroot=[],
                 energy_list={}):
        self.method = method
        self.algroot = algroot
        self.energy_list = energy_list
        self.path = {}
        self.path['work'] = path_work
        self.path['data'] = path_data
        # 初始化根目录地址
        # 初始化工作区地址
        self.path['sima'] = '%s/1.sima' % (self.path['work'])
        self.path['reala'] = '%s/2.reala' % (self.path['work'])
        self.path['backa'] = '%s/3.backa' % (self.path['work'])
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
              parent='vpho',
              usediy=0,
              energy='-1',
              option_list=[],
              condor='0'):
        '用来生成sim文件并运行'
        addfolder(method, self.path['sim'])
        addfolder(method, self.path['rtraw'])
        if(2.0000 in self.energy_list):
            self.energy_list[2.0000][1] = 41814
        if(dopw == ''):
            dosim(txt_folder='%s/%s' % (self.path['sim'], method),
                  dec_folder='%s/%s' % (self.path['dec'], method),
                  rtraw_folder='%s/%s' % (self.path['rtraw'], method),
                  parent=parent,
                  usediy=usediy,
                  energy_list=self.energy_list,
                  energy=energy,
                  files=files,
                  events=events,
                  option_list=option_list,
                  condor=condor)
        else:
            dosim(txt_folder='%s/%s' % (self.path['sim'], method),
                  dec_folder='%s/%s' % (self.path['dec'], method),
                  dat_folder='%s/%s' % (self.path['dec'], method),
                  rtrawfolder='%s/%s' % (self.path['rtraw'], method),
                  parent=parent,
                  usediy=usediy,
                  energy_list=self.energy_list,
                  energy=energy,
                  files=files,
                  events=events,
                  option_list=option_list,
                  condor=condor)

    def dorec(self, method,
              condor='0'):
        '用来生成rec文件并运行'
        addfolder(method, self.path['rec'])
        addfolder(method, self.path['dst'])
        dorec(txt_folder='%s/%s' % (self.path['rec'], method),
              rtraw_folder='%s/%s' % (self.path['rtraw'], method),
              dst_folder='%s/%s' % (self.path['dst'], method),
              condor=condor)

    def dosima(self, method,
               option_list=[],
               condor='0'):
        '用来生成ana文件并运行'
        addfolder(method, self.path['sima'])
        addfolder(method, self.path['simr'])
        doalg(algroot=self.algroot,
              txt_folder='%s/%s' % (self.path['sima'], method),
              root_folder='%s/%s' % (self.path['simr'], method),
              dst_folder='%s/%s' % (self.path['dst'], method),
              options=option_list,
              condor=condor)

# Dst文件分析类函数


def dst_list_rscan():
    # Initial
    output = []
    # Path-1
    path_run = '/bes3fs/offline/data/665p01/rscan/dst'
    for file1 in os.listdir(path_run):
        checkfolder = 0
        if(re.match(r'(\d\d)(\d\d)(\d\d)', file1)):
            checkfolder = 1
        if(1 - checkfolder):
            continue
        for file2 in os.listdir('%s/%s' % (path_run, file1)):
            method1 = r'(\d\d)(\d\d)(\d\d)'
            method2 = r'run_00(\d\d\d\d\d)_All_file(\d\d\d)_SFO-(1|2).dst'
            check1 = re.match(method1, file1)
            check2 = re.match(method2, file2)
            if(check1 and check2):
                output.append({'file_name': file2,
                               'file_path': '%s/%s/%s' % (path_run, file1, file2),
                               'run_number': int(check2.group(1)),
                               'run_id': check2.group(2),
                               'run_year': check1.group(1),
                               'run_month': check1.group(1),
                               'run_day': check1.group(1),
                               'option': []})
    # Path-2
    path_run = '/bes3fs/offline/data/665p01/2175/dst'
    for file1 in os.listdir(path_run):
        checkfolder = 0
        if(re.match(r'(\d\d)(\d\d)(\d\d)', file1)):
            checkfolder = 1
        if(1 - checkfolder):
            continue
        for file2 in os.listdir('%s/%s' % (path_run, file1)):
            method1 = r'(\d\d)(\d\d)(\d\d)'
            method2 = r'run_00(\d\d\d\d\d)_All_file(\d\d\d)_SFO-(1|2).dst'
            check1 = re.match(method1, file1)
            check2 = re.match(method2, file2)
            if(check1 and check2):
                output.append({'file_name': file2,
                               'file_path': '%s/%s/%s' % (path_run, file1, file2),
                               'run_number': int(check2.group(1)),
                               'run_id': check2.group(2),
                               'run_year': check1.group(1),
                               'run_month': check1.group(1),
                               'run_day': check1.group(1),
                               'option': []})
    # Print result
    return output


def dst_list_jpsi():
    # Initial
    output = []
    # Path-1
    path_run = '/besfs4/offline/data/705-1/jpsi/round02/dst'
    for file1 in os.listdir(path_run):
        checkfolder = 0
        if(re.match(r'(\d\d)(\d\d)(\d\d)', file1)):
            checkfolder = 1
        if(1 - checkfolder):
            continue
        for file2 in os.listdir('%s/%s' % (path_run, file1)):
            method1 = r'(\d\d)(\d\d)(\d\d)'
            method2 = r'run_00(\d\d\d\d\d)_All_file(\d\d\d)_SFO-(1|2).dst'
            check1 = re.match(method1, file1)
            check2 = re.match(method2, file2)
            if(check1 and check2):
                output.append({'file_name': file2,
                               'file_path': '%s/%s/%s' % (path_run, file1, file2),
                               'run_number': int(check2.group(1)),
                               'run_id': check2.group(2),
                               'run_year': check1.group(1),
                               'run_month': check1.group(1),
                               'run_day': check1.group(1),
                               'option': []})
    # Print result
    return output


def select_runnumber(datain, run_left, run_right):
    dataout = []
    for i in datain:
        if(i['run_number'] >= run_left and i['run_number'] <= run_right):
            dataout.append(i)
    return dataout


def select_energy(datain, energy):
    dataout = []
    for i in datain:
        if(i['energy'] == energy):
            dataout.append(i)
    return dataout


def cut_length(datain, num):
    dataout = []
    i = 0
    j = 0
    for data in datain:
        if(j >= num):
            i += 1
            j = 0
        if(j == 0):
            dataout.append([])
            dataout[i].append(data)
        else:
            dataout[i].append(data)
        j += 1
    return dataout


def cut_group(datain, num):
    length = int(float(len(datain)) / float(num)) + 1
    dataout = cut_length(datain, length)
    return dataout


def cut_run(folder_txt='',
            folder_root='',
            algroot=[],
            dst_list=[],
            option_list=[],
            do_select_energy=0,
            energy=0,
            do_select_runnumber=0,
            run_number=[0, 0],
            num_group=0,
            num_length=0,
            condor=0):
    '''
    '''
    # 初始化dst序列
    in_dst_list = []
    for i in dst_list:
        in_dst_list.append(i)
    # 选择dst序列
    if(do_select_energy != 0):
        in_dst_list = select_energy(in_dst_list, energy)
    if(do_select_runnumber != 0):
        in_dst_list = select_runnumber(in_dst_list, run_number[0], run_number[1])
    # 重构建dst二维序列
    if(num_group != 0):
        out_list = cut_group(in_dst_list, num_group)
    if(num_length != 0):
        out_list = cut_length(in_dst_list, num_length)
    # 构建option
    in_option_list = option_list + ['%s.Energy = %1.4f' % (algroot[2], energy)]
    # 运行作业
    for count1, i1 in enumerate(out_list):
        dst_list_use = []
        option_list_use = in_option_list
        for count2, i2 in enumerate(out_list[count1]):
            dst_list_use.append(i2['file_path'])
            need_option = 0
            if('option' in i2):
                need_option = 1
            if(need_option != 0):
                for option in i2['option']:
                    if(i2['option'] in option_list_use):
                        continue
                    else:
                        option_list_use += [option]
        alg(algroot=algroot,
            txt_file='%s/%1.4f_%03d.txt' % (folder_txt, energy, count1),
            root_file='%s/%1.4f_%03d.root' % (folder_root, energy, count1),
            dst_list=dst_list_use,
            option_list=option_list_use,
            condor=condor)
        print('Submitting -> |{:^20}|{:^20}|{:^20}|\r'.format('能量点:%.4f' % (energy),
                                                              '作业数:%d' % (count1),
                                                              'Dst长度:%d' % (len(i1))))


def cut_run_number(folder_txt='',
                   folder_root='',
                   algroot=[],
                   dst_list=[],
                   option_list=[],
                   do_select_energy=0,
                   energy=0,
                   do_select_runnumber=0,
                   run_numbers=[],
                   num_group=0,
                   num_length=0,
                   condor=0):
    '''
    '''
    for run_number in run_numbers:
        # 初始化dst序列
        in_dst_list = []
        for i in dst_list:
            in_dst_list.append(i)
        # 选择dst序列
        if(do_select_energy != 0):
            in_dst_list = select_energy(in_dst_list, energy)
        if(do_select_runnumber != 0):
            in_dst_list = select_runnumber(in_dst_list, run_number[0], run_number[1])
        # 重构建dst二维序列
        if(num_group != 0):
            out_list = cut_group(in_dst_list, num_group)
        if(num_length != 0):
            out_list = cut_length(in_dst_list, num_length)
        # 构建option
        in_option_list = option_list + ['%s.Energy = %1.4f' % (algroot[2], energy)]
        # 运行作业
        for count1, i1 in enumerate(out_list):
            dst_list_use = []
            option_list_use = in_option_list
            for count2, i2 in enumerate(out_list[count1]):
                dst_list_use.append(i2['file_path'])
                need_option = 0
                if('option' in i2):
                    need_option = 1
                if(need_option != 0):
                    for option in i2['option']:
                        if(option in option_list_use):
                            continue
                        else:
                            option_list_use += [option]
            alg(algroot=algroot,
                txt_file='%s/%1.4f_%03d_%05d_%05d.txt' % (folder_txt, energy, count1, run_number[0], run_number[1]),
                root_file='%s/%1.4f_%03d_%05d_%05d.root' % (folder_root, energy, count1, run_number[0], run_number[1]),
                dst_list=dst_list_use,
                option_list=option_list_use,
                condor=condor)
            print('Submitting -> |{:^20}|{:^20}|{:^20}|{:^20}|{:^20}|\r'.format('能量点:%.4f' % (energy),
                                                                                '作业数:%d' % (count1),
                                                                                'Dst长度:%d' % (len(i1)),
                                                                                'Run_N left:%d' % (run_number[0]),
                                                                                'Run_N right:%d' % (run_number[1])))


# 统计纠错类函数
def finish_script(filename):
    '检查一个分析code的log文件是否显示完成，返回bool型'
    with open(filename, 'r') as infile:
        lines = infile.readlines()
    check = 0
    for i in lines:
        if(re.match(r'Finish script', i)):
            check = 1
    return check


def check_num_script(folder_script=''):
    '检查一个文件夹中的log文件不同能量点的处理事例数，返回字典'
    filelist = os.listdir(folder_script)
    num = len(filelist) / 3
    num_pass = 0
    output = {}
    for file in filelist:
        print('%d/%d get number\r' % (num_pass, num)),
        method = r'(.*)_(.*).txt.bosslog'
        check = re.match(method, file)
        if(check):
            num_pass += 1
            energy = float(check.group(1))
            with open('%s/%s' % (folder_script, file), 'r') as infile:
                lines = infile.readlines()
            for line in lines:
                checkline = re.search(r'total number:(.*)\n', line)
                if(checkline):
                    number = float(checkline.group(1))
                    if(energy in output):
                        output[energy] += number
                    else:
                        output[energy] = number
    return output


def check_state_script(folder_script=''):
    '检查一个文件夹中所有.txt文件是否有对应完成的.txt.bosslog文件，否则放入返回数组中'
    error = []
    filelist = os.listdir(folder_script)
    num = len(filelist)
    for count, filename in enumerate(filelist):
        print('\rProcess: %d/%d' % (count, num)),
        check = re.match(r'(.*).txt$', filename)
        if(check):
            name = check.group(1)
            name = name + '.txt.bosslog'
            if(name in filelist):
                check_finish = finish_script('script/%s' % (name))
                if(check_finish != 1):
                    error.append(filename)
            else:
                error.append(filename)
    return error
