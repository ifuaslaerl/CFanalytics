classDiagram
    %% Camada de Modelos (Data Structures)
    class Problem {
        +String platform
        +String contest_id
        +String index
        +String name
        +String rating
        +List~String~ tags
        +url() String
        +full_id() String
    }
    class Submission {
        +int id
        +int creation_time_seconds
        +Problem problem
        +String programming_language
        +String verdict
    }
    Submission --> Problem : contains

    %% Camada de Comunicação (Adapter Pattern)
    class PlatformAPI {
        <<interface>>
        +get_user_submissions(handle: String) List~Submission~
    }
    class CodeforcesAPI {
        +BASE_URL: String
        +get_user_submissions(handle) List~Submission~
    }
    class AtCoderAPI {
        +BASE_URL: String
        +get_user_submissions(handle) List~Submission~
    }
    PlatformAPI <|-- CodeforcesAPI
    PlatformAPI <|-- AtCoderAPI

    %% Camada de Negócio (Core Analytics)
    class OmniAnalytics {
        -List~PlatformAPI~ apis
        -List~String~ handles
        -List~Submission~ _submissions
        +load_data()
        +get_upsolving_list() List~Problem~
        +get_verdict_stats() Dict
        +get_language_stats() Dict
    }
    OmniAnalytics o-- PlatformAPI : uses
    OmniAnalytics o-- Submission : processes

    %% Camada de Apresentação (Strategy/Template Pattern para Gráficos)
    class BaseChart {
        <<abstract>>
        +String name
        +OmniAnalytics analytics
        +build_figure()* Figure
        +render(container)
    }
    class VerdictsChart {
        +build_figure() Figure
    }
    class LanguagesChart {
        +build_figure() Figure
    }
    BaseChart <|-- VerdictsChart
    BaseChart <|-- LanguagesChart
    BaseChart --> OmniAnalytics : queries