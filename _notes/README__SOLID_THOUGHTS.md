
### SOLID thoughts:

```
I have refactored the solution (job module) to be more SOLID. But finally met the 'D' which following would be overkill in this small project.
Then apart of Dependence Inversion Principle I have met KISS / DRY and Chat-GPT say me also 'Avoid Premature Optimization'.

But up to that moment I have refactored almost everything ... from this small project.
As this is also way of learning for me, lets go through SOLID principles and what happened duiring refactoring.
```

##### S - SRP - Single Responsibility Principle
```
Classes from jobs module now should have 'more less':
 - only one responsibility
 - so because of this only one reason for change
```

##### O - Open-Closed Principle
```
Do Classes from jobs module follow 'O'?
Not all, for example UrlFetcher is coupled with request module.
But rest 'more less' should follow Open-Closed Principle.
```

##### L - Liskov Substitution Principle
```
Do Classes from jobs module follow 'L'?
So LSP says that descentant-classes should do everything what parent classes do.
I have only one one classes using inheritance... but it follows being detailed.
```

##### I - ISP - Interface Segregation Principle
```
Do Classes from jobs module follow 'I'?
I would say in the right balanced way that not is overkiling.
```

##### D - DIP - Dependency Inversion Principle
```
Do Classes from jobs module follow 'D'?
No.
```


##### Summary from ChatGPT:
```
The SOLID principles are valuable guidelines, especially in larger, team-based, or commercial projects.
But for smaller or solo projects, flexibility is key, and you might not need to fully implement every aspect of these principles.
```
