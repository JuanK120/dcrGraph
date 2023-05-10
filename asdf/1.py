import random


class DCRGraphGenerator:
    def __init__(self, activities, num_relations, num_conditions):
        self.activities = activities
        self.num_relations = num_relations
        self.num_conditions = num_conditions

    def generate(self):
        graph = {
            'activities': self.activities,
            'relations': [],
        }

        # Generate relations
        for _ in range(self.num_relations):
            relation = random.choice(['response', 'condition', 'include','exclude'])
            source = random.choice(self.activities)
            target = random.choice(self.activities)
            graph['relations'].append((relation, source, target))

        return graph


# Example usage
activities = ['A', 'B', 'C', 'D', 'E']
num_relations = 5
num_conditions = 3

generator = DCRGraphGenerator(activities, num_relations, num_conditions)
graph = generator.generate()

print(graph)