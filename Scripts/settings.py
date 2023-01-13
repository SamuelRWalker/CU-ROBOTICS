class Settings:
    def __init__(self,id='Default',generateNumPerPhase=1000,phase1=True,phase2=True,phase3=True,phase4=True,phase5=True,phase6=True):
        self.id = id
        self.generateNumPerPhase = generateNumPerPhase
        self.phase1 = phase1
        self.phase2 = phase2
        self.phase3 = phase3
        self.phase4 = phase4
        self.phase5 = phase5
        self.phase6 = phase6

    def __str__(self):
        return f"{self.id} ({self.generateNumPerPhase}):\n\
        Phase 1: {self.phase1}\n\
        Phase 2: {self.phase2}\n\
        Phase 3: {self.phase3}\n\
        Phase 4: {self.phase4}\n\
        Phase 5: {self.phase5}\n\
        Phase 6: {self.phase6}"