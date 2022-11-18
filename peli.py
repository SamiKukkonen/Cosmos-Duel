from typing import MutableMapping
import pygame
from pygame import event
from pygame.constants import K_DOWN, K_ESCAPE, K_LCTRL, K_LEFT, K_RCTRL, K_RIGHT, K_UP, MOUSEBUTTONDOWN, K_a, K_d, K_s, K_w
from pygame.font import Font
from sys import exit

from pygame.time import Clock
pygame.font.init()
from pygame import mixer
pygame.init()
mixer.init()

LEVEYS = 1280
KORKEUS = 720
RUUTU = pygame.display.set_mode((LEVEYS, KORKEUS))
pygame.display.set_caption("Cosmos Duel")
#pygame.display.set_icon
kello = pygame.time.Clock()

musta = (0,0,0)
oranssi_vari = (255, 95, 31)
vihrea_vari = (0,255,0)
valkoinen = (255,255,255)

FPS = 60
NOPEUS = 10

RAJA = pygame.Rect(LEVEYS//2 - 5,0,10, KORKEUS)

VIHREA_LASERIT = []
ORANSSI_LASERIT = []
LASERIT_NOPEUS = 14
MAX_LASER = 3

MUSIIKKI = True
menu_tausta = mixer.Sound("data/menu.mp3")
menu_tausta.set_volume(0.1)
mixer.music.load("data/tausta.ogg")
osuma_aani = mixer.Sound("data/osuma.mp3")
laser_aani = mixer.Sound("data/laser.mp3")
nappi_aani = mixer.Sound("data/nappi.mp3")
nappi_aani.set_volume(0.2)
osuma_aani.set_volume(0.2)
laser_aani.set_volume(0.2)
pygame.mixer.music.set_volume(0.1)


ISO =  pygame.image.load("data/1920TS.png")
KESKI =  pygame.image.load("data/1280TS.png")
PIENI = pygame.image.load("data/800TS.png")
VIHREA_ALUS_KUVA = pygame.image.load("data/vihrea_alus_t.png")
ORANSSI_ALUS_KUVA = pygame.image.load("data/oranssi_alus_t.png")
AVARUUS_TAUSTA = pygame.image.load("data/avaruus_tausta.jpg")
MENU_TAUSTA = pygame.image.load("data/tausta.jpg")
MENU_START = pygame.image.load("data/start_tarkka.png")
OTSIKKO = pygame.image.load("data/Otsikko_tarkka.png")
VALIKKO = pygame.image.load("data/valikko.png")
VALIKKO_TAUSTA = pygame.image.load("data/tausta_tumma.png")
MUTE = pygame.image.load("data/mute.png")
UNMUTE = pygame.image.load("data/unmute.png")
VIHREA_ALUS_LEVEYS, VIHREA_ALUS_KORKEUS = LEVEYS//12, KORKEUS//8
ORANSSI_ALUS_LEVEYS, ORANSSI_ALUS_KORKEUS = LEVEYS//12, KORKEUS//8

VIHREA_ALUS = pygame.transform.scale(VIHREA_ALUS_KUVA,(VIHREA_ALUS_LEVEYS, VIHREA_ALUS_KORKEUS))
ORANSSI_ALUS = pygame.transform.scale(ORANSSI_ALUS_KUVA,(ORANSSI_ALUS_KORKEUS, ORANSSI_ALUS_LEVEYS))

VIHREA_OSUMA = pygame.USEREVENT + 1
ORANSSI_OSUMA = pygame.USEREVENT + 2

FONTTI = pygame.font.SysFont("comicsans", 30)
VOITTO_FONTTI = pygame.font.SysFont("Helvetica", 80)

class Nappi():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		komento = False
		# Hiirein sijainnin hakeminen
		pos = pygame.mouse.get_pos()
    
		# Tarkistetaan onko hiiri kuvakkeen päälle ja onko klikattu

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				komento = True
		# Napin piirtäminen pinnalle
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return komento 

def menu():
    START_OIKEA = pygame.transform.scale(MENU_START,(LEVEYS/1.2, KORKEUS/1))
    VALIKKO_OIKEA = pygame.transform.scale(VALIKKO,(LEVEYS, KORKEUS/2.6))
    start_button = Nappi(LEVEYS/2.0, KORKEUS/1.9, START_OIKEA, 0.13)
    valikko = Nappi(LEVEYS/2.07, KORKEUS/2.25, VALIKKO_OIKEA, 0.14)
    MENU_TAUSTA_OIKEA = pygame.transform.scale(MENU_TAUSTA,(LEVEYS, KORKEUS))
    OTSIKKO_OIKEA = pygame.transform.scale(OTSIKKO, (LEVEYS//2, KORKEUS//8))
    mixer.music.stop()
    run = True
    while run:
        RUUTU.blit(MENU_TAUSTA_OIKEA, (0,0))
        RUUTU.blit(OTSIKKO_OIKEA,(LEVEYS/2.4 - KORKEUS/4.5, 30))
        if valikko.draw(RUUTU):
            nappi_aani.play()
            menu_tausta.stop()
            asetukset()
            run = False
        if start_button.draw(RUUTU):
            nappi_aani.play()
            main()
            run = False
        if MUSIIKKI:
            menu_tausta.play(0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


def piirto(vihrea, oranssi, VIHREA_LASERIT, ORANSSI_LASERIT, VIHREA_HP, ORANSSI_HP):
    AVARUUS_TAUSTA_OIKEA = pygame.transform.scale(AVARUUS_TAUSTA,(LEVEYS, KORKEUS))
    RUUTU.blit(AVARUUS_TAUSTA_OIKEA,(0,0))
    pygame.draw.rect(RUUTU, musta,RAJA)
    vihrea_hp_teksti = FONTTI.render("♥" * VIHREA_HP, 1, valkoinen)
    oranssi_hp_teksti = FONTTI.render("♥" * ORANSSI_HP, 1, valkoinen)
    RUUTU.blit(vihrea_hp_teksti,(LEVEYS - vihrea_hp_teksti.get_width()-10, 10))
    RUUTU.blit(oranssi_hp_teksti,(10,10))
    RUUTU.blit(ORANSSI_ALUS, (oranssi.x, oranssi.y))
    RUUTU.blit(VIHREA_ALUS,(vihrea.x, vihrea.y))
    for laseri in VIHREA_LASERIT:
        pygame.draw.rect(RUUTU, vihrea_vari, laseri)
    for laseri in ORANSSI_LASERIT:
        pygame.draw.rect(RUUTU, oranssi_vari, laseri)
    pygame.display.update()

def vihrea_liike(painetut_napit, vihrea):
        if painetut_napit[K_a] and vihrea.x - NOPEUS > 0: # Vihreä liike vasemmalle
            vihrea.x -= NOPEUS
        if painetut_napit[K_d] and vihrea.x + NOPEUS + VIHREA_ALUS_LEVEYS < RAJA.x: # Vihreä liike oikealle
            vihrea.x += NOPEUS
        if painetut_napit[K_w] and vihrea.y - NOPEUS > 0: # Vihreä liike ylös      
            vihrea.y -= NOPEUS
        if painetut_napit[K_s] and vihrea.y + NOPEUS + VIHREA_ALUS_KORKEUS < KORKEUS: # Vihreä liike alas  
            vihrea.y += NOPEUS
def oranssi_liike(painetut_napit, oranssi):
        if painetut_napit[K_LEFT] and oranssi.x - NOPEUS > RAJA.x: # Oranssi liike vasemmalle
            oranssi.x -= NOPEUS
        if painetut_napit[K_RIGHT] and oranssi.x + NOPEUS + ORANSSI_ALUS_LEVEYS < LEVEYS + LEVEYS//70: # Oranssi liike oikealle
            oranssi.x += NOPEUS
        if painetut_napit[K_UP] and oranssi.y > 0: # Oranssi liike ylös      
            oranssi.y -= NOPEUS
        if painetut_napit[K_DOWN] and oranssi.y + NOPEUS + ORANSSI_ALUS_KORKEUS < KORKEUS - KORKEUS//70: # Oranssi liike alas  
            oranssi.y += NOPEUS

def laserit_liike(VIHREA_LASERIT, ORANSSI_LASERIT, vihrea, oranssi):
    for laseri in VIHREA_LASERIT:
        laseri.x += LASERIT_NOPEUS
        if oranssi.colliderect(laseri):
            pygame.event.post(pygame.event.Event(ORANSSI_OSUMA))
            if MUSIIKKI:
                osuma_aani.play()
            VIHREA_LASERIT.remove(laseri)
            
        elif laseri.x > LEVEYS:
            VIHREA_LASERIT.remove(laseri)

    for laseri in ORANSSI_LASERIT:
        laseri.x -= LASERIT_NOPEUS
        if vihrea.colliderect(laseri):
            pygame.event.post(pygame.event.Event(VIHREA_OSUMA))
            if MUSIIKKI:
                osuma_aani.play()
            ORANSSI_LASERIT.remove(laseri)
        elif laseri.x < 0:
            ORANSSI_LASERIT.remove(laseri)

def pelin_lopetus(voittaja):

    VIHREA_LASERIT.clear()
    ORANSSI_LASERIT.clear()
    teksti = VOITTO_FONTTI.render(voittaja, 1, valkoinen)
    RUUTU.blit(teksti, (LEVEYS/2 - teksti.get_width()/2, KORKEUS/2 - teksti.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)  
    main()

def main():
    mixer.stop()
    VIHREA_HP = 5
    ORANSSI_HP = 5
    vihrea = pygame.Rect(10, 60, VIHREA_ALUS_LEVEYS, VIHREA_ALUS_KORKEUS)
    oranssi = pygame.Rect(LEVEYS - VIHREA_ALUS_KORKEUS, KORKEUS - ORANSSI_ALUS_KORKEUS * 1.2, VIHREA_ALUS_LEVEYS, VIHREA_ALUS_KORKEUS)
    if MUSIIKKI:
        mixer.music.play(-1)
    run = True
    while run:
        kello.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    menu()
                if event.key == pygame.K_LCTRL and len(VIHREA_LASERIT) < MAX_LASER:
                    if MUSIIKKI:
                        laser_aani.play()
                    laseri = pygame.Rect(vihrea.x + VIHREA_ALUS_LEVEYS, vihrea.y + VIHREA_ALUS_KORKEUS//2 - 2, LEVEYS//60 , KORKEUS//100)
                    VIHREA_LASERIT.append(laseri)
                if event.key == pygame.K_RCTRL and len(ORANSSI_LASERIT) < MAX_LASER:
                    if MUSIIKKI:
                        laser_aani.play()
                    laseri = pygame.Rect(oranssi.x, oranssi.y + ORANSSI_ALUS_KORKEUS//2 + 5, LEVEYS//60 ,KORKEUS//100)
                    ORANSSI_LASERIT.append(laseri)

            if event.type == VIHREA_OSUMA:
                ORANSSI_HP -= 1
            if event.type == ORANSSI_OSUMA:
                VIHREA_HP -=1
        voittaja = ""
        if VIHREA_HP <= 0:
            voittaja = "GREEN WON"
        if ORANSSI_HP <= 0:
            voittaja = "ORANGE WON"
        if voittaja != "":
            pelin_lopetus(voittaja)
            break
        painetut_napit = pygame.key.get_pressed()
        vihrea_liike(painetut_napit, vihrea)
        oranssi_liike(painetut_napit, oranssi)
        piirto(vihrea, oranssi, VIHREA_LASERIT, ORANSSI_LASERIT, VIHREA_HP, ORANSSI_HP)
        laserit_liike(VIHREA_LASERIT, ORANSSI_LASERIT, vihrea, oranssi)

def asetukset():
    nappi_aani.play()
    MUTE_OIKEA = pygame.transform.scale(MUTE, (LEVEYS/10, KORKEUS/6))
    UNMUTE_OIKEA = pygame.transform.scale(UNMUTE, (LEVEYS/10, KORKEUS/6))
    VALIKKO_TAUSTA_OIKEA = pygame.transform.scale(VALIKKO_TAUSTA,(LEVEYS, KORKEUS))
    ISO_OIKEA = pygame.transform.scale(ISO, (LEVEYS, KORKEUS/3))
    KESKI_OIKEA = pygame.transform.scale(KESKI, (LEVEYS, KORKEUS/3))
    PIENI_OIKEA = pygame.transform.scale(PIENI, (LEVEYS, KORKEUS/3))
    iso_nappi = Nappi(LEVEYS/2.5, KORKEUS/3, ISO_OIKEA, 0.3)
    keski_nappi = Nappi(LEVEYS/2.5, KORKEUS/4.5, KESKI_OIKEA, 0.3)
    pieni_nappi = Nappi(LEVEYS/2.5, KORKEUS/8.8, PIENI_OIKEA, 0.3)
    mute_nappi = Nappi(LEVEYS/4, KORKEUS/2, MUTE_OIKEA, 1)
    unmute_nappi = Nappi(LEVEYS/1.35, KORKEUS/2, UNMUTE_OIKEA, 1)
    run = True
    while run:
        RUUTU.blit(VALIKKO_TAUSTA_OIKEA, (0, 0))
        if iso_nappi.draw(RUUTU):
            nappi_aani.play()
            muunto(1920, 1000, 2, 3)
            menu()
            run = False
        if keski_nappi.draw(RUUTU):
            nappi_aani.play()
            muunto(1280,720, 1, 2)
            menu()
            run = False
        if pieni_nappi.draw(RUUTU):
            nappi_aani.play()
            muunto(800,480, 0.5, 1)
            menu()
            run = False
        if mute_nappi.draw(RUUTU):
            nappi_aani.play()
            global MUSIIKKI
            MUSIIKKI = False
            menu()
        if unmute_nappi.draw(RUUTU):
            nappi_aani.play()
            MUSIIKKI = True
            menu()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
                    break
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()
def muunto(x: int, y: int, z: int, f: int):
    global RAJA, KORKEUS, LEVEYS, RUUTU, VIHREA_ALUS_LEVEYS, VIHREA_ALUS_KORKEUS, ORANSSI_ALUS_LEVEYS, ORANSSI_ALUS_KORKEUS, VIHREA_ALUS,ORANSSI_ALUS, NOPEUS, LASERIT_NOPEUS, FONTTI
    LEVEYS = x
    KORKEUS = y
    RUUTU = pygame.display.set_mode((LEVEYS, KORKEUS))
    VIHREA_ALUS_LEVEYS, VIHREA_ALUS_KORKEUS = LEVEYS//12, KORKEUS//8
    ORANSSI_ALUS_LEVEYS, ORANSSI_ALUS_KORKEUS = LEVEYS//12, KORKEUS//8
    VIHREA_ALUS = pygame.transform.scale(VIHREA_ALUS_KUVA,(VIHREA_ALUS_LEVEYS, VIHREA_ALUS_KORKEUS))
    ORANSSI_ALUS = pygame.transform.scale(ORANSSI_ALUS_KUVA,(ORANSSI_ALUS_KORKEUS, ORANSSI_ALUS_LEVEYS))
    RAJA = pygame.Rect(LEVEYS//2 - 5,0,10, KORKEUS)
    NOPEUS = 10 * z
    LASERIT_NOPEUS = 14 * z
    FONTTI = pygame.font.SysFont("comicsans", 30*f)
    print(NOPEUS)
menu()

if __name__ == "__menu__":
    menu()
