package com.google.lint.check;

import com.google.common.base.Joiner;
import com.google.common.collect.ImmutableSet;
import com.google.inject.Inject;
import com.google.lint.common.Context;
import com.google.lint.common.FamilyMetadata;
import com.google.lint.common.FontMetadata;
import com.google.lint.common.FontStore;
import com.google.lint.common.LintCheck;
import com.google.lint.common.MetadataStore;
import com.google.lint.common.Severity;
import com.google.typography.font.sfntly.Font;
import com.google.typography.font.sfntly.Tag;
import com.google.typography.font.sfntly.table.core.PostScriptTable;

import java.io.File;
import java.util.List;
import java.util.Set;

/**
 * @author tocman@gmail.com (Jeremie Lenfant-Engelmann)
 */
public class CheckCanonicalStyles implements LintCheck {

  private static final Set<String> CANONICAL_STYLE_VALUES = ImmutableSet.<String>builder()
      .add("normal")
      .add("italic")
      .build();
  private static final String CANONICAL_STYLE_VALUES_STRING = Joiner.on(", ")
      .join(CANONICAL_STYLE_VALUES);

  private final MetadataStore metadataStore;
  private final FontStore fontStore;

  @Inject
  public CheckCanonicalStyles(MetadataStore metadataStore, FontStore fontStore) {
    this.metadataStore = metadataStore;
    this.fontStore = fontStore;
  }

  @Override
  public void run(Context context, List<String> familyDirectories) {
    for (String familyDirectory : familyDirectories) {
      FamilyMetadata familyMetadata = metadataStore.getFamilyMetadata(familyDirectory);
      for (FontMetadata fontMetadata : familyMetadata.getFontsMetadata()) {
        checkCanonicalStyle(context, familyDirectory, fontMetadata);
        checkStyleMatchesInFontFile(context, familyDirectory, fontMetadata);
      }
    }
  }

  private void checkCanonicalStyle(
      Context context, String familyDirectory, FontMetadata fontMetadata) {
    String fontStyle = fontMetadata.getStyle();
    if (!CANONICAL_STYLE_VALUES.contains(fontStyle)) {
      context.report(Severity.ERROR,
          String.format("%s: Style is \"%s\" for %s which is not one of the canonical values" +
              " (%s)", new File(familyDirectory, "METADATA.json").getPath(), fontStyle,
              fontMetadata.getFilename(), CANONICAL_STYLE_VALUES_STRING));
    }
  }

  private void checkStyleMatchesInFontFile(
      Context context, String familyDirectory, FontMetadata fontMetadata) {
    String filePath = new File(familyDirectory, fontMetadata.getFilename()).getPath();
    Font font = fontStore.getSfntlyFont(familyDirectory, fontMetadata);
    PostScriptTable postTable = font.getTable(Tag.post);
    int angle = postTable.italicAngle();
    String fontStyle = fontMetadata.getStyle();

    if (angle == 0) {
      if (!"normal".equals(fontStyle)) {
        context.report(Severity.ERROR, String.format("%s: The font style is %s but it should " +
            "be normal", filePath, fontStyle));
      }
    } else {
      if (!"italic".equals(fontStyle)) {
        context.report(Severity.ERROR, String.format("%s: The font style is %s but it should " +
            "be italic", filePath, fontStyle));
      }
    }
  }
}
