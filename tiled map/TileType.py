class TerrainType():

    def __init__(self, name, stats, bmp_pos):
        self.bmp = bmp_pos
        self.terrain_name = name
        self.stats = stats
    
    def __repr__(self):
        return self.terrain_name

    def get_cost(self):
        return self.stats["COST"]
    
    def get_bmp(self):
        return self.bmp

class Plains(TerrainType):

    def __init__(self):
        terrain_name = "Plains"
        
        stats = {
            "DEF":0,
            "AVO":0,
            "HEAL":0,
            "DMG":0,
            "COST":1
        }

        bmp_pos = (8,12)

        super().__init__(terrain_name, stats, bmp_pos)

class Forest(TerrainType):

    def __init__(self):
        terrain_name = "Forest"
        
        stats = {
            "DEF":0,
            "AVO":15,
            "HEAL":0,
            "DMG":0,
            "COST":2
        }

        bmp_pos = (26,21)

        super().__init__(terrain_name, stats, bmp_pos)

class Lava(TerrainType):

    def __init__(self):
        terrain_name = "Lava"
        
        stats = {
            "DEF":0,
            "AVO":0,
            "HEAL":0,
            "DMG":5,
            "COST":1
        }

        bmp_pos = (24,16)

        super().__init__(terrain_name, stats, bmp_pos)

class Altar(TerrainType):

    def __init__(self):
        terrain_name = "Altar"
        
        stats = {
            "DEF":0,
            "AVO":0,
            "HEAL":5,
            "DMG":0,
            "COST":1
        }

        bmp_pos = (22,16)

        super().__init__(terrain_name, stats, bmp_pos)

class Miasma(TerrainType):

    def __init__(self):
        terrain_name = "Miasma"
        
        stats = {
            "DEF":2,
            "AVO":-15,
            "HEAL":0,
            "DMG":10,
            "COST":3
        }

        bmp_pos = (8,3)

        super().__init__(terrain_name, stats, bmp_pos)