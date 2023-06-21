
class UpScaler:
    # constructor
    def __init__(self,frames, frames_to_generate: int):
        self.frames_to_generate = frames_to_generate
        self.frames = frames

    def up_scale(self):
        print (self.frames_to_generate)

    def learn_D(self):
        for mol_type in ["CD45","LCK", "TCR"]:
            #TODO: add func
            pass

    def learn_r(self):
        for couple in ["CD45_LCK","CD45_TCR","LCK_TCR"]:
            #TODO: add func
            pass
    def learn_k(self):
        for couple in ["CD45_LCK","CD45_TCR","LCK_TCR"]:
            #TODO: add func
            pass
    def learn_drest(self):
        for couple in ["CD45_LCK","CD45_TCR","LCK_TCR"]:
            #TODO: add func
            pass


if __name__ == '__main__':
    frames_to_generate = 10
    up_scaler = UpScaler(frames_to_generate)
    up_scaler.up_scale()

