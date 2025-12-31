from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, Literal, List, Union, Annotated, Any



class EScapyConfigModel(BaseModel):
  pass


# -------------------- UI FIELD TYPES --------------------
class UIField(BaseModel):
  label: str
  info: str = ""
  value: Any


class InputField(UIField):
  type: Literal["input"] = "input"
  value: str = ""

  itype: Literal['text', 'password'] = "text"

  placeholder: str = ""

  required: bool = False
  minlength: Optional[int] = None
  maxlength: Optional[int] = None
  pattern: Optional[str] = None
  
  prefix: Optional[str] = None


class TextAreaField(UIField):
  type: Literal["textarea"] = "textarea"
  value: str = ""
  
  placeholder: str = ""

  required: bool = False
  minlength: Optional[int] = None
  maxlength: Optional[int] = None
  rows: int = 3
  
  prefix: Optional[str] = None


class ColorField(UIField):
  type: Literal["color"] = "color"
  value: str

  prefix: Optional[str] = None


class NumberField(UIField):
  type: Literal["number"] = "number"
  value: Union[int, float] = 0
  
  placeholder: str = ""

  min: Optional[Union[int, float]] = None
  max: Optional[Union[int, float]] = None
  step: Optional[Union[int, float]] = 1
  
  prefix: Optional[str] = None


class RangeField(UIField):
  type: Literal["range"] = "range"
  value: Union[int, float]

  min: Union[int, float]
  max: Union[int, float]
  step: Optional[Union[int, float]] = 1


class SelectField(UIField):
  type: Literal["select"] = "select"
  value: str

  required: bool = False
  options: Dict[str, str]
  
  prefix: Optional[str] = None


class CheckboxField(UIField):
  type: Literal["checkbox"] = "checkbox"
  value: bool


class ToggleField(UIField):
  type: Literal["toggle"] = "toggle"
  value: bool


# Special Type returns prefix if value or empty string
class FlagInputField(UIField):
  type: Literal["flag"] = "flag"
  value: bool = False
  
  prefix: Optional[str] = None


UIControl = Annotated[
  Union[
    InputField,
    TextAreaField,
    CheckboxField,
    ToggleField,
    NumberField,
    RangeField,
    SelectField,
    ColorField,
    
    FlagInputField
  ],
  Field(discriminator="type")
]

# -------------------- Task --------------------
class CreateTaskOptionsModel(BaseModel):
  once: bool            # run once
  autostart: bool       # auto start task on create

  signal: Optional[str] = None
  delay: Optional[float] = None

  repeat: Optional[float] = None
  repeat_count: Optional[float] = None

  options: Dict[str, Any] = {}  # Module options


class CreateTaskModel(BaseModel):
  name: str
  module: str
  # Task config
  config: CreateTaskOptionsModel = Field(default_factory=CreateTaskOptionsModel)

# -------------------- Module --------------------
MSG_TYPES = Literal['text', 'html', 'raw_html']


class ShellCustomMessageModel(BaseModel):
  # Fallback
  fallback: MSG_TYPES | Literal['ignore']

# Module Config run
class ShellOptionsModel(BaseModel):
  # str for shell type
  command: str

  shell: bool = False
  # user to use
  user: str = "nobody"
  # message 
  message: MSG_TYPES | ShellCustomMessageModel = "text"


# Module Config
class ModuleConfigModel(BaseModel):
  # Title
  title: str
  # Author
  author: str
  # About
  about: str = ""
  # Icon
  icon: str = "icon.png"
  # Dashboard path
  dashboard: str = "dashboard"
  # Run command - string for script path
  run: ShellOptionsModel | str
  
  # Module Task Options - scheme
  options: Optional[Dict[str, UIControl]] = None


class LoginRequest(BaseModel):
  access_key: str

