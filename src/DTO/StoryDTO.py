from Model.Story import Story, Module, ModuleResponse


class ModuleResponseDTO:
    def __init__(self, module_response: ModuleResponse):
        self.success = module_response.success
        self.fail = module_response.fail


class ModuleDTO:
    def __init__(self, module: Module):
        self._id = str(module._id)
        self.name = module.name
        self.position = module.position
        self.description = module.description
        self.response = ModuleResponseDTO(module.response)
        self.components = module.components
        self.time_max = module.time_max
        self.win_condition = module.win_condition
        self._type = module._type


class StoryDTO:
    def __init__(self, story: Story):
        self.user_id = str(story.user_id)
        self.character_name = story.character_name
        self.stage = story.stage
        self.modules = []
        for m in story.modules:
            self.modules.append(ModuleDTO(m))
        self.components = story.components
        self.companion_name = story.companion_name
        self.life = story.life
