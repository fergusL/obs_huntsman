'''
Override the default characterise config parameters by putting them in here.
e.g.:
config.doWrite = False
'''
config.doWrite = False
config.doOverscan = False
# config.doAddDistortionModel = False
config.doDefect = False
config.doAssembleIsrExposures = False
config.doBias = False
config.doDark = False
config.doFlat = False
config.doSaturationInterpolation = False

# Below are the default isr config parameters/values
# config.isr.saveMetadata = True
# config.isr.datasetType = 'raw'
# config.isr.fallbackFilterName = None
# config.isr.useFallbackDate = False
# config.isr.expectWcs = True
# config.isr.fwhm = 1.0
# config.isr.doConvertIntToFloat = True
# config.isr.doSaturation = True
# config.isr.saturatedMaskName = 'SAT'
# config.isr.saturation = nan
# config.isr.growSaturationFootprintSize = 1
# config.isr.doSuspect = False
# config.isr.suspectMaskName = 'SUSPECT'
# config.isr.numEdgeSuspect = 0
# config.isr.doSetBadRegions = True
# config.isr.badStatistic = 'MEANCLIP'
# config.isr.doOverscan = True
# config.isr.overscanFitType = 'MEDIAN'
# config.isr.overscanOrder = 1
# config.isr.overscanNumSigmaClip = 3.0
# config.isr.overscanIsInt = True
# config.isr.overscanNumLeadingColumnsToSkip = 0
# config.isr.overscanNumTrailingColumnsToSkip = 0
# config.isr.overscanMaxDev = 1000.0
# config.isr.overscanBiasJump = False
# config.isr.overscanBiasJumpKeyword = 'NO_SUCH_KEY'
# config.isr.overscanBiasJumpDevices = []
# config.isr.overscanBiasJumpLocation = 0
# config.isr.doAssembleCcd = True
# config.isr.doAssembleIsrExposures = False
# config.isr.doTrimToMatchCalib = False
# config.isr.doBias = True
# config.isr.biasDataProductName = 'bias'
# config.isr.doVariance = True
# config.isr.gain = nan
# config.isr.readNoise = 0.0
# config.isr.doEmpiricalReadNoise = False
# config.isr.doLinearize = True
# config.isr.doCrosstalk = False
# config.isr.doCrosstalkBeforeAssemble = False
# config.isr.doDefect = True
# config.isr.doNanMasking = True
# config.isr.doWidenSaturationTrails = True
# config.isr.doBrighterFatter = False
# config.isr.brighterFatterLevel = 'DETECTOR'
# config.isr.brighterFatterMaxIter = 10
# config.isr.brighterFatterThreshold = 1000.0
# config.isr.brighterFatterApplyGain = True
# config.isr.brighterFatterMaskGrowSize = 0
# config.isr.doDark = True
# config.isr.darkDataProductName = 'dark'
# config.isr.doStrayLight = False
# config.isr.doFlat = True
# config.isr.flatDataProductName = 'flat'
# config.isr.flatScalingType = 'USER'
# config.isr.flatUserScale = 1.0
# config.isr.doTweakFlat = False
# config.isr.doApplyGains = False
# config.isr.normalizeGains = False
# config.isr.doFringe = True
# config.isr.fringeAfterFlat = True
# config.isr.doMeasureBackground = False
# config.isr.doCameraSpecificMasking = False
# config.isr.doInterpolate = True
# config.isr.doSaturationInterpolation = True
# config.isr.doNanInterpolation = True
# config.isr.doNanInterpAfterFlat = False
# config.isr.maskListToInterpolate = ['SAT', 'BAD', 'UNMASKEDNAN']
# config.isr.doSaveInterpPixels = False
# config.isr.fluxMag0T1 = {'Unknown': 158489319246.11172}
# config.isr.defaultFluxMag0T1 = 158489319246.11172
# config.isr.doVignette = False
# config.isr.doAttachTransmissionCurve = False
# config.isr.doUseOpticsTransmission = True
# config.isr.doUseFilterTransmission = True
# config.isr.doUseSensorTransmission = True
# config.isr.doUseAtmosphereTransmission = True
# config.isr.doIlluminationCorrection = False
# config.isr.illuminationCorrectionDataProductName = 'illumcor'
# config.isr.illumScale = 1.0
# config.isr.illumFilters = []
# config.isr.doWrite = False
