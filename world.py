from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from scene import Scene

class World(Scene):
    def __init__(self, is_current_scene) -> None:
        super().__init__(is_current_scene)

    def world_gen(self):
        grass_texture = load_texture('assets/grass_block.png')
        stone_texture = load_texture('assets/stone_block.png')
        brick_texture = load_texture('assets/brick_block.png')
        dirt_texture  = load_texture('assets/dirt_block.png')
        sky_texture   = load_texture('assets/skybox.png')
        arm_texture   = load_texture('assets/arm_texture.png')
        punch_sound   = Audio('assets/punch_sound',loop = False, autoplay = False)
        background_music = Audio('assets/background-music', loop = True, autoplay = True)
        success_sound = Audio('assets/task_success.wav', loop = False, autoplay= False)
        background_music.volume = 0.3
        self.block_pick = 1


        noiseScale  = 0.02
        scale = 20
        noise = PerlinNoise()

        class Task(Button):
            def __init__(self,taskName, position = (0,0), success_sound = success_sound):
                super().__init__(
                    parent = camera.ui,
                    model = 'quad',
                    text = taskName,
                    position = position
                )

                self.first_time = False
                self.success_sound = success_sound
                self.fit_to_text()

            def submit(self):
                self.success_sound.play()
                destroy(self)

        self.create_blocks = Task('Create blocks with left click', position = (-.7,.4))
        self.right_click = Task('Destroy blocks with right cick', position = (-.7,.3))
        self.switch_items = Task('Switch Items with numpad 1 to 4', position = (-.7,.2))

        class Voxel(Button):
            def __init__(self, world: World,position = (0,0,0),texture = grass_texture):
                super().__init__(
                    parent = scene,
                    position = position,
                    model = 'assets/block',
                    origin_y = 0.5,
                    texture = texture,
                    color = color.color(0,0,random.uniform(0.9,1)),
                    scale = 0.5)
                
                self.world = world

            def input(self,key):
                if self.hovered:
                    if key == 'left mouse down':
                        punch_sound.play()
                        if self.world.block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture,world=self.world)
                        if self.world.block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture,world=self.world)
                        if self.world.block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture,world=self.world)
                        if self.world.block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture,world=self.world)

                    if key == 'right mouse down':
                        punch_sound.play()
                        destroy(self)

        class Hand(Entity):
            def __init__(self):
                super().__init__(
                    parent = camera.ui,
                    model = 'assets/arm',
                    texture = arm_texture,
                    scale = 0.2,
                    rotation = Vec3(150,-10,0),
                    position = Vec2(0.4,-0.6))

            def active(self):
                self.position = Vec2(0.3,-0.5)

            def passive(self):
                self.position = Vec2(0.4,-0.6)

        for z in range(scale):
            for x in range(scale):
                noiseVal = round(noise([z * noiseScale,x * noiseScale]) * scale)
                if noiseVal < 2: voxel = Voxel(world=self,position = (x,noiseVal,z), texture = stone_texture)
                elif noiseVal > 1:  voxel = Voxel(world=self,position = (x,noiseVal,z))

        vel = 10
        self.player = FirstPersonController(speed=vel)
        sky = Sky()
        self.hand = Hand()

    def update(self):

        if held_keys['shift']:
            vel = 15
        
        if held_keys['left mouse']:
            self.hand.active()

            if self.create_blocks: self.create_blocks.submit()
        elif held_keys['right mouse']:
            self.hand.active()
        
            if self.right_click: self.right_click.submit()
        else:
            self.hand.passive()


            if self.player.y < -50:
                Text(
                    parent = camera.ui,
                    text = 'GAME OVER!',
                    scale = (2,2,2)

                )

                

        if self.block_pick > 1:
            if self.switch_items:
               self.switch_items.submit()
        if held_keys['1']: self.block_pick = 1
        if held_keys['2']: self.block_pick = 2
        if held_keys['3']: self.block_pick = 3
        if held_keys['4']: self.block_pick = 4
