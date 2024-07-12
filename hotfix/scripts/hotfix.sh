#!/bin/bash
set -x

# Set Variables stage
echo "Tag: $Tag"

major=$(echo $Tag | cut -d. -f1)
minor=$(echo $Tag | cut -d. -f2)
patch=$(echo $Tag | cut -d. -f3)
# version=$($(echo "$Tag" | tr '.' '\n'))
# echo "Major: ${version[0]} , Minor: ${version[1]} , Patch: ${version[2]}"

if [ "$patch" != "0" ]; then
  echo "Hotfix branch can be created only from the official build!"
  echo "i.e. Tag should be x.y.0 (actual Tag: $Tag)"
  exit 1
fi


Branch="hotfix-$Tag"
echo "Branch=$Branch"
if [ "$minor" == "0" ]; then
  echo "Old Versioning"
  Version="$major.$patch"
  echo "Version=$Version"
else
  echo "New Versioning"
  Version="$major.$minor"
  echo "Version=$Version"
fi

Channel="GLCP-HF"
# Creating hotfix branch and making required changes 
git checkout -b hotfix-$Tag 
git branch
git status


# Create ci_merge_hotfix-<Tag>.yaml stage
echo "This stage is to create ci_merge_hotfix-$Tag.yaml"
if [ -f "managed-ci/hotfix/template/managed-ci-hotfix.yaml" ]; then
  cp -prv managed-ci/hotfix/template/managed-ci-hotfix.yaml .github/workflows/managed-ci-hotfix-$Tag.yaml
  sed -i 's/^\(\s*VERSION\s*:\s*\).*/\1'\"$Version\"'/' .github/mci-variables.yaml
  sed -i 's/^\(\s*VERSION_MINOR\s*:\s*\).*/\1'\"$minor\"'/' .github/mci-variables.yaml
  sed -i 's/^\(\s*VERSION_MAJOR\s*:\s*\).*/\1'\"$major\"'/' .github/mci-variables.yaml
  sed -i 's/^\(\s*CHANNEL\s*:\s*\).*/\1'\"$Channel\"'/' .github/mci-variables.yaml
  sed -i "s/- hotfix/- hotfix-$Tag/g" .github/workflows/managed-ci-hotfix-$Tag.yaml
  sed -i "s/HOTFIX/HOTFIX-$Tag/g" .github/workflows/managed-ci-hotfix-$Tag.yaml
else 
 echo "workflow doesnot exit"
 exit 1
fi
 
# Git Push stage
git add .github/workflows/managed-ci-hotfix-$Tag.yaml .github/mci-variables.yaml
git commit -m "added hotfix workflow"
git push -u origin hotfix-$Tag