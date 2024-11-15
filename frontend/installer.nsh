Function .onInit
  SetDetailsPrint both
  ShowInstDetails show
FunctionEnd

!macro customInit
  InstallDir "$PROGRAMFILES\GuestLiangElectronApp"
  BrandingText "© 2024 GuestLiang"
!macroend

Section "MainSection" SecMain
  !insertmacro customInit
SectionEnd
