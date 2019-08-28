from Model.Story import Story, Module, ModuleResponse, ModuleAnswer


class ModuleResponseDTO:
    def __init__(self, module_response: ModuleResponse):
        self.success = module_response.success
        self.fail = module_response.fail


class ModuleAnswerDTO:
    def __init__(self, answer: ModuleAnswer):
        self.text = answer.text
        try:
            destination = int(answer.destination)
        except ValueError:
            destination = 0
        self.destination = destination


class ModuleDTO:
    def __init__(self, module: Module):
        self._id = str(module._id)
        self.name = module.name
        self.position = module.position
        self.description = module.description
        self.response = ModuleResponseDTO(module.response)
        self.time_max = module.time_max
        self.win_condition = module.win_condition
        self._type = module._type
        self.answers = []
        for a in module.answers:
            self.answers.append(ModuleAnswerDTO(a))


class StoryDTO:
    def __init__(self, story: Story):
        self.user_id = str(story.user_id)
        self.title = story.title
        self.character_name = story.character_name
        self.stage = story.stage
        self.modules = []
        for m in story.modules:
            self.modules.append(ModuleDTO(m))
        self.companion_name = story.companion_name
        self.life = story.life
