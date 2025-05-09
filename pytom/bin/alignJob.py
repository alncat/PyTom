#!/usr/bin/env pytom
'''
Created on Jan 30, 2013

@author: Thomas Hrabe
'''

if __name__ == '__main__':
    # parse command line arguments

    import sys
    from pytom.tools.script_helper import ScriptHelper, ScriptOption
    from pytom.tools.parse_script_options import parse_script_options
    from pytom.tools.files import checkFileExists,checkDirExists
    
    helper = ScriptHelper(sys.argv[0].split('/')[-1], 
                          description='Create an alignment job. Documentation is available at\n\
                          http://www.pytom.org/doc/pytom/alignment.html',
                          authors='Thomas Hrabe',
                          options=[ScriptOption(['-p','--particleList'], 'Particle list : xml file storing information to all subvolumes', arg=True, optional=False),
                                   ScriptOption(['-r','--reference'], 'Reference : the alignment reference', arg=True, optional=False),
                                   ScriptOption(['-m','--mask'], 'Mask : a mask ', arg=True, optional=False),
                                   ScriptOption(['--angleShells'], '# angle shells used for angular refinement.', arg=True, optional=False),
                                   ScriptOption(['--angleIncrement'], 'Angular increment for refinement.', arg=True, optional=False),
                                   ScriptOption(['--symmetry'], 'PointSymmetry : specify n-fold symmetry (n)', arg=True, optional=True),
                                   ScriptOption(['--symmetryAngleZ'], 'PointSymmetry axis tilt around Z axis', arg=True, optional=True),
                                   ScriptOption(['--symmetryAngleX'], 'PointSymmetry axis tilt around X axis', arg=True, optional=True),
                                   ScriptOption(['-l','--lowestFrequency'], 'Highest frequency band used : in pixels', arg=True, optional=False),
                                   ScriptOption(['-h','--highestFrequency'], 'Lowest frequency band used : in pixels', arg=True, optional=False),
                                   ScriptOption(['-d','--destination'], 'Destination : destination directory', arg=True, optional=False),
                                   ScriptOption(['-n','--numberIterations'], 'Number of iterations', arg=True, optional=False),
                                   ScriptOption(['-b','--binning'], 'Perform binning (downscale) of subvolumes: 1: no binning, 2: 2 pixels -> 1, 3: 3 -> 1 ...', arg=True, optional=False),
                                   ScriptOption(['--pixelSize'], 'Pixelsize in Angstrom', arg=True, optional=False),
                                   ScriptOption(['--particleDiameter'], 'Particle diameter in Angstrom', arg=True, optional=False),
                                   ScriptOption(['-j','--jobName'], 'Specify job.xml filename', arg=True, optional=False),
                                   ScriptOption(['-h', '--help'], 'Help.', arg=False, optional=True)])
    
    if len(sys.argv) <= 2:
        print(helper)
        sys.exit()
    try:
        particleList, reference, mask, angShells,angleInc,symmetryN,symmetryAxisZ,symmetryAxisX,\
        lowestFrequency,highestFrequency,destination,numberIterations,binning,\
        pixelSize,diameter,jobName,help = parse_script_options(sys.argv[1:], helper)
    except Exception as e:
        print(e)
        sys.exit()
        
    if help is True:
        print(helper)
        sys.exit()
        
    if not checkFileExists(particleList):
        raise RuntimeError('ParticleList file ' + volume + ' does not exist!')
    
    if not checkFileExists(reference):
        raise RuntimeError('Reference file ' + reference + ' does not exist!')
    
    if not checkFileExists(mask):
        raise RuntimeError('Mask file ' + mask + ' does not exist!')
    
    if not checkDirExists(destination):
        raise RuntimeError('Destination directory ' + destination + ' does not exist!')    

    from pytom.alignment.ExMaxAlignment import ExMaxJob
    from pytom.basic.structures import ParticleList,Reference,Mask,SampleInformation,PointSymmetry
    from pytom.basic.score import FLCFScore
    # from pytom.frontend.serverpages.createAlignmentJob import createRunscripts
    from pytom.angles.localSampling import LocalSampling
    from pytom.alignment.preprocessing import Preprocessing
     
    p       = ParticleList()
    p.fromXMLFile(particleList)
    r       = Reference(reference)
    m       = Mask(mask)
    a       = LocalSampling(angShells,angleInc)
    pre     = Preprocessing(lowestFrequency = float(lowestFrequency),highestFrequency = float(highestFrequency))
    sample  = SampleInformation(pixelSize = float(pixelSize), particleDiameter = float(diameter))
    
    if symmetryN is None or symmetryAxisZ is None or symmetryAxisX is None:
        sym = None
    else:
        sym = PointSymmetry(nfold=int(symmetryN),z2=float(symmetryAxisZ),x=float(symmetryAxisX))
    
    job = ExMaxJob(particleList=p,destination=destination,reference=r,score=FLCFScore(),
                   rotations=a,mask=m,symmetry=sym,
                   numberRefinementRounds=None,numberIterations=numberIterations,preprocessing=pre,
                   excludeThreshold=-1,binning=int(binning),sampleInformation=sample,fscCriterion=0.5,
                   adaptiveResolution=True,adaptiveOffset=0.1,angleFactor=0.5)

    
    job.toXMLFile(jobName)
    
    # createRunscripts(jobName[:-3] + 'sh',jobName)
    
    
    
    
    
