from numpy import linspace
from os import path
from random import shuffle
import pygame as pg

from button import Button
from constants import consts as c
from text import Text


class UpgradeManager:
    def __init__(self):
        self.completed_upgrades = []
        self.load_possible_upgrades()

    def get_random_upgrades(self):
        upgrades = []

        for upgrade in self.possible_upgrades:
            if upgrade["pre_req"] is None:
                upgrades.append(upgrade)
            else:
                pre_req = upgrade["pre_req"]
                flag = True
                if "upgrade" in pre_req and not pre_req["upgrade"] in self.completed_upgrades:
                    flag = False
                if "level" in pre_req and c.player.level < pre_req["level"]:
                    flag = False

                if flag:
                    upgrades.append(upgrade)

        if len(upgrades) <= c.max_upgrades:
            return upgrades
        else:
            shuffle(upgrades)
            return upgrades[:c.max_upgrades]
        
    def render_upgrade_elements(self, upgrade, x_coord):
        title_text = Text(x_coord, c.s_height // 4, upgrade["name"], c.screen)
        title_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), 30))
        
        description_text = Text(x_coord, 3 * c.s_height // 4 - 20, upgrade["description"], c.screen)
        description_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), 20))

        effect_text = Text(x_coord, 3 * c.s_height // 4, f"Effect: {upgrade['effect'][0]}x -> {upgrade['effect'][1]}x", c.screen)
        effect_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), 20))

        icon_image = pg.image.load(path.join(path.dirname(__file__), "assets", "icons", upgrade["icon"]))
        icon_image = pg.transform.scale(icon_image, (200, 200))
        icon_rect = pg.Rect(x_coord - 100, c.s_height // 2 - 100, 200, 200)

        button = Button(x_coord, 3 * c.s_height // 4 + 100, 100, 40, c.screen, "Evolve")
        button.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), 20))

        self.text_elements.append(title_text)
        self.icons.append(icon_image)
        self.icon_rects.append(icon_rect)
        self.text_elements.append(description_text)
        self.text_elements.append(effect_text)
        self.buttons.append(button)

    def implement_upgrade(self, upgrade):
        current_value = getattr(c, upgrade["target"])
        if upgrade["effect"][0] == 0:
            new_value = upgrade["effect"][1]
        else:
            new_value = current_value * upgrade["effect"][1] / upgrade["effect"][0]

        setattr(c, upgrade["target"], new_value)

        c.player.reload_properties()
        self.possible_upgrades.remove(upgrade)
        self.completed_upgrades.append(upgrade["name"])

    def show_upgrade_screen(self):
        upgrades = self.get_random_upgrades()
        upgrade_x = linspace(0, c.s_width, len(upgrades) + 2)[1:-1]

        title_text = Text(c.s_width // 2, c.s_height // 8, f"Generation {c.player.level}", c.screen)
        title_text.set_font(pg.font.Font(path.join(path.dirname(__file__), "assets", "orbitron.ttf"), c.title_font_size))

        self.text_elements = [title_text]
        self.icons = []
        self.icon_rects = []
        self.buttons = []

        for upgrade, x_coord in zip(upgrades, upgrade_x):
            self.render_upgrade_elements(upgrade, x_coord)

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, button in enumerate(self.buttons):
                            button.check_clicked(pg.mouse.get_pos(), 1)
                            if button.left_clicked:
                                self.implement_upgrade(upgrades[i])
                                running = False

            c.screen.fill(c.black)

            for text in self.text_elements:
                text.render()

            for icon, icon_rect in zip(self.icons, self.icon_rects):
                c.screen.blit(icon, icon_rect)

            for button in self.buttons:
                button.render()

            pg.display.flip()

    def load_possible_upgrades(self):
        self.possible_upgrades = [
            # max health upgrades
            {
                "name": "Plasma Membrane I",
                "icon": "plasma_membrane.png",
                "description": "Increases membrane health",
                "effect": [1.0, 1.2],
                "target": "player_max_health",
                "pre_req": None,
            },
            {
                "name": "Plasma Membrane II",
                "icon": "plasma_membrane.png",
                "description": "Increases membrane health",
                "effect": [1.2, 1.4],
                "target": "player_max_health",
                "pre_req": {
                    "upgrade": "Plasma Membrane I"
                }
            },
            {
                "name": "Plasma Membrane III",
                "icon": "plasma_membrane.png",
                "description": "Increases membrane health",
                "effect": [1.4, 1.6],
                "target": "player_max_health",
                "pre_req": {
                    "upgrade": "Plasma Membrane II"
                }
            },
            {
                "name": "Plasma Membrane IV",
                "icon": "plasma_membrane.png",
                "description": "Increases membrane health",
                "effect": [1.6, 1.8],
                "target": "player_max_health",
                "pre_req": {
                    "upgrade": "Plasma Membrane III"
                }
            },
            {
                "name": "Plasma Membrane V",
                "icon": "plasma_membrane.png",
                "description": "Increases membrane health",
                "effect": [1.8, 2],
                "target": "player_max_health",
                "pre_req": {
                    "upgrade": "Plasma Membrane IV"
                }
            },
            # # heal upgrades
            # {
            #     "name": "Anabolism I",
            #     "icon": "anabolism.png",
            #     "description": "Increases health gain from sugar",
            #     "effect": [1.0, 1.5],
            #     "target": "sugar_to_health",
            #     "pre_req": None
            # },
            # {
            #     "name": "Anabolism II",
            #     "icon": "anabolism.png",
            #     "description": "Increases health gain from sugar",
            #     "effect": [1.5, 2.0],
            #     "target": "sugar_to_health",
            #     "pre_req": {
            #         "upgrade": "Anabolism I"
            #     }
            # },
            # {
            #     "name": "Anabolism III",
            #     "icon": "anabolism.png",
            #     "description": "Increases health gain from sugar",
            #     "effect": [2.0, 2.5],
            #     "target": "sugar_to_health",
            #     "pre_req": {
            #         "upgrade": "Anabolism II"
            #     }
            # },
            # # energy yield upgrades
            # {
            #     "name": "Krebs' Cycle",
            #     "icon": "mitochondria.png",
            #     "description": "Increases ATP yield from sugar",
            #     "effect": [1.0, 2.0],
            #     "target": "sugar_to_atp",
            #     "pre_req": None
            # },
            # {
            #     "name": "Photosynthesis",
            #     "icon": "photosynthesis.png",
            #     "description": "Passively synthesize sugar",
            #     "effect": [0, 0.2],
            #     "target": "sugar_synthesis_rate",
            #     "pre_req": {
            #         "level": 5
            #     }
            # },
            # # movement upgrade
            # {
            #     "name": "Cilia",
            #     "icon": "cilia.png",
            #     "description": "Increases max speed",
            #     "effect": [1.0, 2.0],
            #     "target": "player_max_v",
            #     "pre_req": None
            # },
            # # combat upgrade
            # {
            #     "name": "Antibody",
            #     "icon": "antibody.png",
            #     "description": "Hit enemies from a distance",
            #     "effect": [0, 1],
            #     "target": "antibody",
            #     "pre_req": None
            # },
            # {
            #     "name": "Cytokine Storm",
            #     "icon": "cytokine.png",
            #     "description": "A storm that damages everything",
            #     "effect": [0, 1],
            #     "target": "storm",
            #     "pre_req": {
            #         "level": 5
            #     }
            # },
            # # defense upgrade
            # {
            #     "name": "Cytoskeleton",
            #     "icon": "cytoskeleton.png",
            #     "description": "Reduce damage taken from contact",
            #     "effect": [1.0, 0.5],
            #     "target": "contact_damage_multiplier",
            #     "pre_req": None
            # },
            {
                "name": "Protein Coat",
                "icon": "coat.png",
                "description": "Reduce damage taken from antibodies",
                "effect": [1.0, 0.5],
                "target": "antibody_damage_multiplier",
                "pre_req": None
            },
            # # faster level-up upgrades
            # {
            #     "name": "DNA Polymerase",
            #     "icon": "dna_polymerase.png",
            #     "description": "Less ATP required for replication",
            #     "effect": [1.0, 0.75],
            #     "target": "atp_req_multiplier",
            #     "pre_req": None
            # },
            # {
            #     "name": "Centrosome",
            #     "icon": "anaphase.png",
            #     "description": "Less ATP required for replication",
            #     "effect": [0.75, 0.5],
            #     "target": "atp_req_multiplier",
            #     "pre_req": {
            #         "upgrade": "DNA Polymerase"
            #     }
            # },
            # # increase pick-up upgrades
            # {
            #     "name": "Endocytosis",
            #     "icon": "endocytosis.png",
            #     "description": "Increased sugar pick-up",
            #     "effect": [1.0, 2.0],
            #     "target": "sugar_multiplier",
            #     "pre_req": None
            # },
            # # sensing upgrade
            # {
            #     "name": "Chemotaxis",
            #     "icon": "chemotaxis.png",
            #     "description": "Enemy directions are shown",
            #     "effect": [0, 1],
            #     "target": "chemotaxis",
            #     "pre_req": {
            #         "level": 5
            #     }
            # },
            # {
            #     "name": "Glycophilia",
            #     "icon": "glucose.png",
            #     "description": "Attract sugar",
            #     "effect": [0, 1],
            #     "target": "glycophilia",
            #     "pre_req": {
            #         "level": 5
            #     }
            # },
            # # respawn upgrade
            # {
            #     "name": "Plasmid",
            #     "icon": "plasmid.png",
            #     "description": "Respawn (once) after death",
            #     "effect": [0, 1],
            #     "target": "respawn",
            #     "pre_req": {
            #         "level": 10
            #     }
            # },
        ]


upgrade_manager = UpgradeManager()
            

        